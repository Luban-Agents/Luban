import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from luban.agent_core import (
    DefaultAgent,
    InMemoryMemory,
    SubtaskVerifier,
    TaskSkillPlanner,
)
from luban.backends.skills.robosyn import RoboSynPolicyBackend
from luban.environments.benchmarks.robosynchallenge import (
    RoboSynChallengeEnvironment,
)
from luban.exceptions import BackendError, ConfigError, EnvironmentError
from luban.pipelines import SkillExecutionPipeline
from luban.runtimes import SyncRuntime

np = pytest.importorskip("numpy")


class Tensor(np.ndarray):
    """Small CPU tensor stand-in so adapter contracts need no optional Torch."""

    def detach(self):
        return self

    def to(self, *, dtype, device):
        return self.astype(dtype).view(Tensor)

    def unsqueeze(self, axis):
        return np.expand_dims(self, axis)

    def permute(self, *axes):
        return self.transpose(axes)

    def contiguous(self):
        return np.ascontiguousarray(self).view(Tensor)


def tensor(value, dtype=None, device=None):
    return np.asarray(value, dtype=dtype).view(Tensor)


@pytest.fixture
def fake_torch(monkeypatch):
    import importlib

    original_import = importlib.import_module
    torch = SimpleNamespace(
        as_tensor=tensor,
        device=lambda value: SimpleNamespace(
            type=value.split(":")[0],
            index=int(value.split(":")[1]) if ":" in value else None,
        ),
        cuda=SimpleNamespace(set_device=Mock()),
        float32=np.float32,
        bool=np.bool_,
        isfinite=np.isfinite,
        inference_mode=nullcontext,
    )
    monkeypatch.setattr(
        importlib,
        "import_module",
        lambda name, *args: torch if name == "torch" else original_import(name, *args),
    )
    return torch


class GymEnvironment:
    def __init__(self, success_frame=3, horizon=5, fail_frame=None):
        self.unwrapped = self
        self.device = "cpu"
        self.single_action_space = SimpleNamespace(shape=(14,))
        self.sim = Mock()
        self.sim_cfg = SimpleNamespace(physics_dt=0.01)
        self.success_frame = success_frame
        self.fail_frame = fail_frame
        self.horizon = horizon
        self.frames = 0
        self.actions = []
        self.resets = []
        self.get_info_calls = 0
        self.closed = False

    def get_obs(self):
        return {
            "robot": {"qpos": np.zeros((1, 14), dtype=np.float32)},
            "sensor": {
                "cam_high": {"color": np.full((1, 2, 3, 4), 255, dtype=np.uint8)}
            },
            "extra": {"privileged_pose": [1, 2, 3]},
        }

    def reset(self, *, seed, options):
        self.resets.append((seed, options))
        self.frames = 0
        return self.get_obs(), self.get_info()

    def get_info(self):
        self.get_info_calls += 1
        return {
            # Native auto-reset can reset this tensor to zero on timeout.
            "elapsed_steps": tensor([0 if self.frames >= self.horizon else self.frames])
        }

    def step(self, action):
        self.actions.append(np.asarray(action))
        self.frames += 1
        truncated = self.frames >= self.horizon
        return (
            self.get_obs(),
            0,
            self.frames == self.fail_frame,
            truncated,
            self.get_info(),
        )

    def get_wrapper_attr(self, name):
        assert name == "is_task_success"
        return lambda: self.frames >= self.success_frame

    def close(self):
        self.closed = True


@pytest.fixture
def environment(tmp_path, fake_torch):
    config_dir = tmp_path / "configs" / "click_bell" / "clear"
    config_dir.mkdir(parents=True)
    (config_dir / "gym_config.json").write_text(
        '{"id":"ClickBell", "max_episode_steps":5}'
    )
    (config_dir.parent / "action_config.json").write_text("{}")
    gym = GymEnvironment()
    env = RoboSynChallengeEnvironment(
        tmp_path,
        environment_factory=lambda config, gym_config, action_config: (
            gym,
            gym_config,
        ),
    )
    env._upstream = SimpleNamespace(
        prepare_episode_reset=Mock(side_effect=lambda env, seed: seed),
        extract_instruction_from_gym_config=lambda cfg: "Click the bell",
        suppress_expert_output=nullcontext,
        check_episode_feasibility=Mock(
            return_value={"feasible": True, "expert_plan_steps": 10}
        ),
    )
    return env


def policy(action_dim=14):
    return Mock(
        config=SimpleNamespace(image_features={"observation.images.cam_high": {}}),
        parameters=lambda: iter([SimpleNamespace(device="cpu")]),
        select_action=Mock(return_value=tensor(np.zeros((1, action_dim)))),
    )


@pytest.mark.parametrize(
    "policy_name, device",
    [("act", "cuda:5"), ("dp", "cuda:5"), ("act", "cuda"), ("act", "cpu")],
)
def test_policy_load_uses_device_type_and_moves_to_requested_gpu(
    fake_torch, monkeypatch, policy_name, device
):
    import importlib

    original_import = importlib.import_module
    model = policy()
    policy_class = SimpleNamespace(from_pretrained=Mock(return_value=model))
    policy_module = SimpleNamespace(
        ACTPolicy=policy_class, DiffusionPolicy=policy_class
    )
    monkeypatch.setattr(
        importlib,
        "import_module",
        lambda name, *args: (
            policy_module
            if name.startswith("lerobot.policies.")
            else original_import(name, *args)
        ),
    )
    backend = RoboSynPolicyBackend(
        "test-checkpoint", policy_name=policy_name, device=device
    )
    backend._load_policy()
    overrides = policy_class.from_pretrained.call_args.kwargs["cli_overrides"]
    assert overrides[0] == f"--device={device.split(':')[0]}"
    assert "--device=cuda:5" not in overrides
    if policy_name == "dp":
        assert "--num_inference_steps=10" in overrides
    model.to.assert_called_once()
    requested_device = model.to.call_args.args[0]
    assert requested_device.type == device.split(":")[0]
    if device == "cuda:5":
        assert requested_device.index == 5
        fake_torch.cuda.set_device.assert_called_once_with(requested_device)
    else:
        fake_torch.cuda.set_device.assert_not_called()
    model.eval.assert_called_once()


def test_reset_uses_upstream_seed_and_omits_privileged_state(environment):
    task = {"name": "click_bell", "seed": 17, "episode_index": 1}
    assert environment.check_episode_feasibility(task)["feasible"]
    first = environment.reset(task)
    second = environment.reset(task)
    assert environment.env.resets == [(17, {"save_data": False})] * 2
    assert environment._upstream.prepare_episode_reset.call_count == 2
    assert first["episode_id"] != second["episode_id"]
    assert set(first["policy_observation"]) == {"robot", "sensor"}
    assert first["available_skills"] == ["click_bell"]
    assert first["head_rgb"].shape == (2, 3, 3)
    environment.env.sim.update.assert_called_with(0.01, 1)
    assert environment.env.get_info_calls == 4
    assert environment.env.actions == []
    assert environment.metadata()["reset_state_protocol"] == (
        "warmup_get_obs_get_info_v2"
    )
    assert environment.episode_metadata()["reset_state_protocol"] == (
        "warmup_get_obs_get_info_v2"
    )


def test_zero_warmup_keeps_native_reset_without_an_extra_state_evaluation(environment):
    environment.reset_sync_steps = 0
    environment.reset({"name": "click_bell", "seed": 0})
    assert environment.env.get_info_calls == 1
    assert environment.env.actions == []
    environment.env.sim.update.assert_not_called()
    environment._upstream.prepare_episode_reset.assert_called_once_with(
        environment.env, 0
    )


@pytest.mark.parametrize("warmup, origin_frame", [(1, 1), (0, 2)])
def test_warmup_consumes_initial_skip_before_first_action_origin_capture(
    environment, warmup, origin_frame
):
    class StatefulGymEnvironment(GymEnvironment):
        def __init__(self):
            super().__init__()
            self.skip_first_eval = True
            self.origin_frame = None

        def reset(self, **kwargs):
            result = super().reset(**kwargs)
            # Native task reset clears these after the base reset evaluates state.
            self.skip_first_eval = True
            self.origin_frame = None
            return result

        def get_info(self):
            result = super().get_info()
            first_eval = self.skip_first_eval
            self.skip_first_eval = False
            if not first_eval and self.origin_frame is None:
                self.origin_frame = self.frames
            return result

    gym = StatefulGymEnvironment()
    environment.environment_factory = lambda config, gym_config, action_config: (
        gym,
        gym_config,
    )
    environment.reset_sync_steps = warmup
    environment.reset({"name": "click_bell", "seed": 0})
    assert gym.origin_frame is None
    assert gym.get_info_calls == 1 + warmup
    for _ in range(origin_frame):
        environment.execute({"actions": np.zeros((1, 14))})
    assert gym.origin_frame == origin_frame
    assert len(gym.actions) == origin_frame


def test_action_chunk_stops_on_authoritative_success(environment):
    environment.reset({"name": "click_bell", "seed": 0})
    result = environment.execute({"actions": np.zeros((5, 14))})
    assert result["task_success"] and result["done"]
    assert result["executed_steps"] == result["environment_steps"] == 3
    assert result["env_info"]["success"] is True
    assert len(environment.env.actions) == 3
    with pytest.raises(EnvironmentError, match="Reset"):
        environment.execute({"actions": np.zeros((1, 14))})


def test_timeout_keeps_actual_steps_and_rejects_same_frame_success(environment):
    environment.reset({"name": "click_bell", "seed": 0})
    environment.env.success_frame = 5
    result = environment.execute({"actions": np.zeros((5, 14))})
    assert not result["task_success"] and result["done"]
    assert result["env_info"]["success"] is False
    assert result["env_feedback"] == "horizon"
    assert environment.episode_metadata()["environment_steps"] == 5


@pytest.mark.parametrize(
    "actions",
    [[], np.zeros((1, 32)), np.full((1, 14), np.nan), np.ones((1, 14), dtype=bool)],
)
def test_invalid_actions_never_reach_native_step(environment, actions):
    environment.reset({"name": "click_bell", "seed": 0})
    with pytest.raises(EnvironmentError, match="Invalid"):
        environment.execute({"actions": actions})
    assert environment.env.actions == []


def test_policy_preprocessing_queue_reset_and_strict_action_dimension(environment):
    model = policy()
    backend = RoboSynPolicyBackend("test-checkpoint", policy=model)
    obs = environment.reset({"name": "click_bell", "seed": 0})
    inputs = {"observation": obs, "skill": "click_bell"}
    backend.predict(inputs)
    backend.predict(inputs)
    assert model.reset.call_count == 1
    batch = model.select_action.call_args.args[0]
    assert batch["observation.state"].shape == (1, 14)
    assert batch["observation.images.cam_high"].shape == (1, 3, 2, 3)
    assert np.max(batch["observation.images.cam_high"]) == 1
    inputs["observation"] = environment.reset({"name": "click_bell", "seed": 0})
    backend.predict(inputs)
    assert model.reset.call_count == 2
    model.select_action.return_value = tensor(np.zeros((1, 32)))
    with pytest.raises(BackendError, match="expected"):
        backend.predict(inputs)


@pytest.fixture
def catalog_backend(environment, tmp_path, monkeypatch):
    import importlib

    models = {"click_bell": policy(), "water_pouring": policy()}
    for value, model in zip((0.25, 0.75), models.values(), strict=True):
        model.select_action.return_value = tensor(np.full((1, 14), value))
    paths = {skill: tmp_path / skill for skill in models}
    for path in paths.values():
        path.mkdir()
    loader = Mock(side_effect=lambda path, **kwargs: models[Path(path).name])
    original_import = importlib.import_module
    monkeypatch.setattr(
        importlib,
        "import_module",
        lambda name, *args: (
            SimpleNamespace(ACTPolicy=SimpleNamespace(from_pretrained=loader))
            if name == "lerobot.policies.act.modeling_act"
            else original_import(name, *args)
        ),
    )
    return RoboSynPolicyBackend(checkpoint_paths=paths, device="cpu"), models, loader


def test_planner_catalog_selection_changes_actions_for_the_same_observation(
    environment, catalog_backend
):
    backend, models, loader = catalog_backend
    observation = environment.reset({"name": "click_bell", "seed": 0})
    inputs = {"observation": observation, "skill": "click_bell"}
    first = backend.predict(inputs)
    assert np.all(first["actions"] == 0.25)
    assert first["policy_selection"]["selection_mode"] == "planner_catalog"
    backend.predict(inputs)
    assert loader.call_count == 1
    inputs["skill"] = "water_pouring"
    second = backend.predict(inputs)
    assert observation["task_name"] == "click_bell"
    assert np.all(second["actions"] == 0.75)
    assert second["policy_selection"]["skill"] == "water_pouring"
    assert second["policy_selection"]["reset_reason"] == "skill_changed"
    assert loader.call_count == 2
    assert all(model.reset.call_count == 1 for model in models.values())


def test_catalog_retry_resets_queue_but_same_skill_replan_preserves_it(
    environment, catalog_backend
):
    backend, models, _ = catalog_backend
    inputs = {
        "observation": environment.reset({"name": "click_bell", "seed": 0}),
        "skill": "click_bell",
        "session_id": "first",
        "execution_id": "execution-1",
        "attempt_id": "execution-1:attempt:1",
    }
    assert (
        backend.predict(inputs)["policy_selection"]["reset_reason"] == "episode_start"
    )
    assert backend.predict(inputs)["policy_selection"]["reset_reason"] is None
    inputs.update(execution_id="execution-2", attempt_id="execution-2:attempt:1")
    assert backend.predict(inputs)["policy_selection"]["reset_reason"] is None
    inputs["attempt_id"] = "execution-2:attempt:2"
    assert backend.predict(inputs)["policy_selection"]["reset_reason"] == "retry"
    inputs["session_id"] = "second"
    assert (
        backend.predict(inputs)["policy_selection"]["reset_reason"] == "episode_start"
    )
    assert models["click_bell"].reset.call_count == 3


def test_catalog_healthcheck_is_deferred_and_unknown_skill_cannot_fall_back(
    environment, catalog_backend
):
    backend, _, loader = catalog_backend
    assert backend.healthcheck()["healthy"] is True
    loader.assert_not_called()
    with pytest.raises(BackendError, match="catalog"):
        backend.predict(
            {
                "observation": environment.reset({"name": "click_bell", "seed": 0}),
                "skill": "unknown",
            }
        )
    loader.assert_not_called()


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"checkpoint_path": "one", "checkpoint_paths": {"click_bell": "two"}},
        {"checkpoint_paths": {}},
        {"checkpoint_paths": {"": "two"}},
        {"checkpoint_paths": {"click_bell": None}},
    ],
)
def test_checkpoint_configuration_is_unambiguous(kwargs):
    with pytest.raises(ConfigError):
        RoboSynPolicyBackend(**kwargs)


def test_environment_exposes_complete_catalog_without_selecting_policy(environment):
    environment.available_skills = ["click_bell", "water_pouring"]
    observation = environment.reset({"name": "click_bell", "seed": 0})
    assert observation["available_skills"] == ["click_bell", "water_pouring"]
    observation["available_skills"].clear()
    assert environment.available_skills == ["click_bell", "water_pouring"]


def test_framework_runs_one_native_action_and_verification_per_step(
    environment, tmp_path
):
    model = policy()
    agent = DefaultAgent(
        planner=TaskSkillPlanner(),
        verifier=SubtaskVerifier(),
        memory=InMemoryMemory(),
        skill_backend=RoboSynPolicyBackend("test-checkpoint", policy=model),
    )
    runtime = SyncRuntime(max_steps=5, output_dir=tmp_path / "results")
    result = runtime.run(
        agent,
        SkillExecutionPipeline(),
        environment,
        {"name": "click_bell", "seed": 0},
        close_resources=False,
    )
    assert result["success"] and result["termination_reason"] == "task_success"
    assert result["steps"] == 3
    assert model.select_action.call_count == len(environment.env.actions) == 3
    assert model.reset.call_count == 1
    trace = next((tmp_path / "results").glob("*/trace.jsonl")).read_text()
    steps = [
        event
        for line in trace.splitlines()
        if (event := json.loads(line))["event"] == "step"
    ]
    assert len(steps) == 3
    assert all("verification" in event for event in steps)


def test_native_tensor_success_reaches_pipeline_and_runtime(environment, tmp_path):
    original_factory = environment.environment_factory

    def native_tensor_factory(config, gym_config, action_config):
        gym, config = original_factory(config, gym_config, action_config)
        original_info = gym.get_info
        gym.get_info = lambda: {
            **original_info(),
            "success": tensor([gym.frames >= gym.success_frame], dtype=np.bool_),
        }
        return gym, config

    environment.environment_factory = native_tensor_factory
    agent = DefaultAgent(
        planner=TaskSkillPlanner(),
        verifier=SubtaskVerifier(),
        memory=InMemoryMemory(),
        skill_backend=RoboSynPolicyBackend("test-checkpoint", policy=policy()),
    )
    result = SyncRuntime(max_steps=5, output_dir=tmp_path).run(
        agent,
        SkillExecutionPipeline(),
        environment,
        {"name": "click_bell", "seed": 0},
        close_resources=False,
    )
    assert result["success"] is True
    assert result["termination_reason"] == "task_success"
    saved = json.loads(next(tmp_path.glob("*/result.json")).read_text())
    assert saved["success"] is True
    assert saved["last_output"]["verification"]["task_success"] is True


def test_default_sdk_root_matches_third_party_layout(tmp_path):
    robosyn_root = tmp_path / "benchmarks" / "RoboSynChallenge"
    environment = RoboSynChallengeEnvironment(robosyn_root)
    assert environment.embodichain_root == tmp_path / "third_party" / "EmbodiChain"


def test_invalid_task_cannot_escape_config_root(tmp_path):
    environment = RoboSynChallengeEnvironment(tmp_path)
    with pytest.raises(EnvironmentError, match="directory"):
        environment.reset({"name": "../../escape"})
    assert environment._upstream is None

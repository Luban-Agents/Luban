"""Evaluate RoboSynChallenge policies through the Luban closed loop."""

import argparse
import hashlib
import sys
from pathlib import Path

from luban.agent_core import (
    DefaultAgent,
    EnvironmentVerifier,
    InMemoryMemory,
    TaskSkillPlanner,
)
from luban.backends.skills.robosyn import RoboSynPolicyBackend
from luban.config import build_agent, load_yaml
from luban.environments.benchmarks.robosynchallenge import (
    RoboSynChallengeEnvironment,
)
from luban.evals.benchmarks.robosynchallenge import RoboSynChallengeEvaluator
from luban.evals.benchmarks.robosynchallenge.matrix import run_matrix
from luban.observability import LocalEpisodeRecorder
from luban.pipelines import DirectPipeline, SkillExecutionPipeline
from luban.runtimes import SyncRuntime


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robosyn-root", required=True, type=Path)
    parser.add_argument("--embodichain-root", type=Path)
    parser.add_argument("--task")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-revision")
    parser.add_argument("--policy", choices=["act", "dp"], default="act")
    parser.add_argument("--setting", choices=["random", "clear"], default="random")
    parser.add_argument("--output", required=True, type=Path)
    seed_options = parser.add_mutually_exclusive_group()
    seed_options.add_argument("--seeds", nargs="+", type=int)
    seed_options.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--start-seed", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--agent-config", type=Path)
    parser.add_argument("--matrix-manifest", type=Path)
    parser.add_argument("--matrix-gpus", nargs="+", type=int)
    parser.add_argument(
        "--matrix-scheduling", choices=["fixed", "dynamic"], default="fixed"
    )
    parser.add_argument("--pipeline", choices=["direct", "skill"])
    parser.add_argument("--planner-check-interval-chunks", type=int, default=64)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--environment-device", default="cpu")
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--renderer", default="hybrid")
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--reset-sync-steps", type=int, default=1)
    parser.add_argument("--dp-num-inference-steps", type=int, default=10)
    parser.add_argument("--max-steps", type=int, default=10000)
    parser.add_argument("--timeout-seconds", type=float, default=1800)
    parser.add_argument("--record-video", action="store_true")
    parser.add_argument("--video-fps", type=int, default=10)
    args = parser.parse_args()
    if args.matrix_manifest:
        command = [sys.executable, str(Path(__file__).resolve())]
        for key in (
            "robosyn_root",
            "embodichain_root",
            "agent_config",
            "pipeline",
            "planner_check_interval_chunks",
            "device",
            "environment_device",
            "gpu",
            "renderer",
            "reset_sync_steps",
            "dp_num_inference_steps",
            "max_steps",
            "timeout_seconds",
            "video_fps",
        ):
            value = getattr(args, key)
            if value is not None:
                command.extend(["--" + key.replace("_", "-"), str(value)])
        for key in ("display", "record_video"):
            if getattr(args, key):
                command.append("--" + key.replace("_", "-"))
        summary = run_matrix(
            args.matrix_manifest,
            args.output.resolve(),
            command,
            resume=args.resume,
            matrix_gpus=args.matrix_gpus,
            matrix_scheduling=args.matrix_scheduling,
        )
    else:
        if not args.task:
            parser.error("Single-task evaluation requires --task")
        if args.episodes <= 0:
            parser.error("--episodes must be positive")
        if args.planner_check_interval_chunks <= 0:
            parser.error("--planner-check-interval-chunks must be positive")
        seeds = (
            args.seeds
            if args.seeds is not None
            else list(range(args.start_seed, args.start_seed + args.episodes))
        )
        checkpoint = args.checkpoint.resolve() if args.checkpoint else None
        catalog = None
        if args.agent_config:
            config = load_yaml(args.agent_config)
            backend = config.get("skill_backend", {})
            if backend.get("class_path", "").endswith(".RoboSynPolicyBackend"):
                init_args = backend.setdefault("init_args", {})
                catalog = init_args.get("checkpoint_paths")
                if catalog is None:
                    if checkpoint is None:
                        parser.error("Single-checkpoint mode requires --checkpoint")
                    init_args["checkpoint_path"] = str(checkpoint)
                else:
                    # Matrix task labels and checkpoint arguments cannot choose
                    # the executed controller in planner-catalog mode.
                    checkpoint = None
                init_args.update(
                    policy_name=args.policy,
                    device=args.device,
                    dp_num_inference_steps=args.dp_num_inference_steps,
                )
            agent = build_agent(config)
        else:
            if checkpoint is None:
                parser.error("Single-checkpoint mode requires --checkpoint")
            agent = DefaultAgent(
                planner=TaskSkillPlanner(),
                verifier=EnvironmentVerifier(),
                memory=InMemoryMemory(),
                skill_backend=RoboSynPolicyBackend(
                    checkpoint_path=str(checkpoint),
                    policy_name=args.policy,
                    device=args.device,
                    dp_num_inference_steps=args.dp_num_inference_steps,
                ),
            )
        if catalog is None and checkpoint is None:
            parser.error("Single-checkpoint mode requires --checkpoint")
        checkpoint_sha256 = {}
        catalog_metadata = {}
        paths = catalog if catalog is not None else {args.task: str(checkpoint)}
        for skill, checkpoint_path in paths.items():
            resolved_path = Path(checkpoint_path).expanduser().resolve()
            hashes = {}
            for path in sorted(resolved_path.iterdir()):
                if path.is_file():
                    with path.open("rb") as file:
                        hashes[path.name] = hashlib.file_digest(
                            file, "sha256"
                        ).hexdigest()
            if catalog is None:
                checkpoint_sha256 = hashes
            else:
                catalog_metadata[skill] = {
                    "checkpoint_path": str(resolved_path),
                    "sha256": hashes,
                }
        environment = RoboSynChallengeEnvironment(
            robosyn_root=str(args.robosyn_root.resolve()),
            embodichain_root=(
                str(args.embodichain_root.resolve()) if args.embodichain_root else None
            ),
            setting=args.setting,
            device=args.environment_device,
            headless=not args.display,
            renderer=args.renderer,
            gpu_id=args.gpu,
            reset_sync_steps=args.reset_sync_steps,
            available_skills=list(catalog) if catalog is not None else None,
        )
        pipeline_name = args.pipeline or ("skill" if args.agent_config else "direct")
        pipeline = (
            SkillExecutionPipeline(
                planner_check_interval_chunks=args.planner_check_interval_chunks
            )
            if pipeline_name == "skill"
            else DirectPipeline()
        )
        runtime = SyncRuntime(
            output_dir=args.output,
            max_steps=args.max_steps,
            timeout_seconds=args.timeout_seconds,
            observability=LocalEpisodeRecorder(
                record_video=args.record_video,
                video_camera_keys=["head_rgb"],
                video_fps=args.video_fps,
            ),
        )
        evaluator = RoboSynChallengeEvaluator(
            environment,
            args.output,
            args.task,
            seeds,
            setting=args.setting,
            resume=args.resume,
            run_metadata={
                "agent_mode": (
                    "planner_policy_catalog"
                    if catalog is not None
                    else "configured_agent"
                    if args.agent_config
                    else "learned_policy_baseline"
                ),
                "policy": args.policy,
                "checkpoint_path": str(checkpoint) if checkpoint is not None else None,
                "checkpoint_revision": args.checkpoint_revision,
                "checkpoint_sha256": checkpoint_sha256,
                "policy_catalog": catalog_metadata,
                "framework_source_sha256": {
                    name: hashlib.sha256(
                        (Path(__file__).resolve().parents[1] / name).read_bytes()
                    ).hexdigest()
                    for name in (
                        "scripts/eval_robosynchallenge.py",
                        "src/luban/backends/skills/robosyn.py",
                        "src/luban/environments/benchmarks/robosynchallenge/environment.py",
                        "src/luban/evals/benchmarks/robosynchallenge/evaluator.py",
                        "src/luban/pipelines/skill_execution.py",
                        "src/luban/agent_core/planners/subtask_skill.py",
                        "src/luban/agent_core/verifiers/subtask.py",
                    )
                },
                "planner_check_interval_chunks": args.planner_check_interval_chunks,
                "policy_device": args.device,
                "agent_config_sha256": (
                    hashlib.sha256(args.agent_config.read_bytes()).hexdigest()
                    if args.agent_config
                    else None
                ),
                "runtime_max_steps": args.max_steps,
                "runtime_timeout_seconds": args.timeout_seconds,
                "record_video": args.record_video,
            },
        )
        try:
            summary = evaluator.run(agent, pipeline, runtime)
        finally:
            try:
                agent.close()
            finally:
                environment.close()
    if not summary["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

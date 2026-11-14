[English](robosynchallenge.md) · [简体中文](robosynchallenge.zh-CN.md)

# RoboSynChallenge

This integration connects RoboSynChallenge to Luban's runtime, execution and verification flow. It supports task-specific ACT/DP policies, explicit seeds, individual tasks and resumable evaluation matrices. RoboSynChallenge is a laboratory benchmark. The titration video uses a separate Isaac Sim scene.

## Environment and resources

Use a dedicated Python 3.11 simulation environment. Follow [RoboSynChallenge](https://github.com/EDEM-AI/RoboSynChallenge) and [EmbodiChain](https://github.com/DexForce/EmbodiChain) to prepare their SDKs, DexSim, LeRobot, NVIDIA drivers and assets, then install Luban. Reference revisions are RoboSynChallenge `8818c82df5fa2522809b8105e7018950dcc9a9a8` and EmbodiChain `89c14da8d0221dc4ee2a4a3e0ba1078b16d447bd`. Select the public ACT or DP checkpoint for the chosen task.

## Single-checkpoint baseline

Run from the repository root and replace the three resource paths with your installations.

```bash
python scripts/eval_robosynchallenge.py \
  --robosyn-root /path/to/RoboSynChallenge \
  --embodichain-root /path/to/EmbodiChain \
  --task click_bell \
  --checkpoint /path/to/ACT_sim_click_bell \
  --setting random --seeds 0 \
  --device cuda:0 --gpu 0 \
  --output runs/robosyn-click-bell
```

Without an agent config, this is a deterministic `TaskSkillPlanner` / `EnvironmentVerifier` policy baseline. Add `--agent-config configs/agents/robosynchallenge_act_visual.yaml` to enable visual planning and verification around the CLI-selected checkpoint. For model-selected dispatch, use the catalog below. Set `LUBAN_LLM_BASE_URL` and `LUBAN_LLM_MODEL` for a service supporting images and structured output. ACT/DP does not consume the planner's language instruction.

## Model-selected policy catalog

For an agent-driven run, use `robosynchallenge_act_catalog.yaml`. The model sees all
ten task controllers and chooses one from the task instruction and camera image.
That choice loads the selected ACT checkpoint; the environment does not restrict
the catalog to the task label. A retry in the same execution clears ACT's queued
actions. Normal replanning with the same controller preserves the queue. Each
action records `policy_selection`, including the checkpoint and reset reason.
The example allows 1,024 response tokens and asks for concise planning fields so
long replies do not get cut off at the earlier 512-token cap.
ACT consumes images and joint state, so natural-language subtask text does not
condition its low-level movements. This is task-level skill dispatch and visual
supervision, not a language-conditioned policy or newly trained stage controller.

Place the ten released `ACT_sim_*` directories under `LUBAN_ROBOSYN_MODEL_ROOT`.
Run from the repository root with the prepared simulation Python:

```bash
export LUBAN_LLM_BASE_URL=http://127.0.0.1:28000
export LUBAN_LLM_MODEL=Qwen3.5-9B
export LUBAN_ROBOSYN_MODEL_ROOT=/path/to/robosyn-models
python scripts/eval_robosynchallenge.py \
  --robosyn-root /path/to/RoboSynChallenge \
  --embodichain-root /path/to/EmbodiChain \
  --task click_bell --setting random --seeds 0 1 2 \
  --agent-config configs/agents/robosynchallenge_act_catalog.yaml \
  --planner-check-interval-chunks 64 \
  --device cuda:0 --gpu 0 --record-video \
  --output runs/robosyn-catalog-click-bell
```

The included matrix covers ten tasks and seeds 0–2: **30 new episodes**. It is a
functional evaluation, distinct from the historical 1,000-episode result. Set the
manifest's seeds to the complete desired list for a larger evaluation.

```bash
python scripts/eval_robosynchallenge.py \
  --robosyn-root /path/to/RoboSynChallenge \
  --embodichain-root /path/to/EmbodiChain \
  --matrix-manifest configs/runs/robosynchallenge_act_catalog_random.json \
  --matrix-gpus 0 --matrix-scheduling dynamic --record-video \
  --output runs/robosyn-catalog-random
```

## Outputs and resuming

The output directory contains `metadata.json`, `summary.json`, `episodes.jsonl` and per-attempt records. Native environment feedback determines success, and execution errors are counted separately. With the same settings, `--resume` skips valid outcomes and retries interrupted or exceptional episodes. Use a new process and output directory for another task or setting.

Use `--matrix-manifest` for a manifest containing `tasks`, `seeds`, `setting` and `policy`. Single-checkpoint tasks specify `name` and `checkpoint_path`; catalog mode uses `name` and the shared `agent_config`. `--matrix-gpus` selects GPU queues and `--matrix-scheduling dynamic` assigns work to available queues. CPU regression checks cover dispatch, retry, native-result precedence, seed counts, persisted exceptions and resuming. They do not start simulation. See the [results guide](reported-results.md) for the historical 412/1000 result.

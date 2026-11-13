[English](chemistry.md) · [简体中文](chemistry.zh-CN.md)

# Model-driven chemistry demo

The fixed `toy_titration_v1` scene demonstrates a visual agent picking a NaOH
bottle, adding liquid until the beaker becomes pink, returning the bottle and
recording the finding. It uses Isaac Sim 4.5 in a separate Python 3.10 worker;
Luban's planner/client uses Python 3.11. Chemistry is symbolic and arm motion uses
scripted IK primitives. This is a demonstration, not the RoboSyn benchmark.

## Prepare and start

Install the locked client and the worker packages with their own interpreters.
Prepare a Franka USD asset, FFmpeg, an NVIDIA GPU and an image-capable model service.

```bash
uv sync --locked --extra chemistry_bench
"$ISAAC_PYTHON" -m pip install \
  ./benchmarks/chemistry-bench-proto ./benchmarks/chemistry-bench-sim
CHEMISTRY_BENCH_SIM_GPU=0 CHEMISTRY_BENCH_FRANKA_USD="$FRANKA_USD" \
  "$ISAAC_PYTHON" -m chemistry_bench_sim.worker --port 50061 \
  --record-dir "$PWD/runs/chemistry-model/continuous" \
  --kit-args --portable-root "$PWD/runs/chemistry-model/kit-cache"
```

Set `ISAAC_PYTHON` to Isaac's `python.sh` and `FRANKA_USD` to its asset path.
Select a GPU with enough free memory. Kit and CUDA device numbering must agree;
on this tested multi-GPU host, GPU 0 with `CUDA_VISIBLE_DEVICES=0` avoids lengthy
cross-device validation. Keep the unauthenticated loopback worker dedicated to
this run. Startup and licensed asset preparation remain operator actions.

## Run the model

From another terminal in the repository root:

```bash
.venv/bin/python scripts/smoke_chemistry_bench.py \
  --address 127.0.0.1:50061 --output runs/chemistry-model/runtime \
  --agent-config configs/agents/chemistry_bench_titration.yaml \
  --base-url http://127.0.0.1:28000 --episodes 1 --rpc-timeout 600 \
  --timeout-seconds 3600
```

Passing `--agent-config` is essential: without it, the smoke runner uses a fixed
script. In model mode, each selected skill becomes the actual RPC primitive;
the agent receives a fresh camera image and verification after every action.
Privileged pH and volumes remain grading-only. Native success requires pink liquid
and a recorded finding. Returning the bottle is an instruction, not an extra
grading condition. A model claim cannot establish success.

The run config supplies a normalized `detail_crop` for this fixed camera. The model
receives the full current frame and a 512×512 enlargement of its beaker region;
recorded video keeps the full scene. This uses RGB pixels only and does not track
objects or synthesize colors. If the camera/layout changes, update or disable the
crop. The smoke runner uses that same run-config crop and exposes a wall-clock
budget for slow shared GPUs. Earlier full-frame-only attempts are retained in the
validation record rather than counted as successful demonstrations.

`smoke_summary.json`, `agent_trace.jsonl`, Runtime video and the worker's continuous
video provide the evidence. Continuous video uses simulation time and omits model
inference pauses. Keep failed attempts. An RPC timeout invalidates the client;
reconcile or restart the dedicated worker before another attempt.

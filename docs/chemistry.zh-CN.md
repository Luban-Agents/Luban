[English](chemistry.md) · [简体中文](chemistry.zh-CN.md)

# 模型驱动的化学仿真 Demo

固定场景 `toy_titration_v1` 展示视觉智能体抓取 NaOH 瓶、加液至烧杯变粉红、归位并
记录现象。Isaac Sim 4.5 worker 使用独立 Python 3.10，Luban 规划器与客户端使用
Python 3.11。化学状态采用符号模型，机械臂执行脚本化 IK 原语。这是演示场景，
与 RoboSyn benchmark 分别运行。

## 准备与启动

使用各自解释器安装锁定的客户端和 worker。另需 Franka USD 资产、FFmpeg、
NVIDIA GPU，以及支持图像输入的模型服务。

```bash
uv sync --locked --extra chemistry_bench
"$ISAAC_PYTHON" -m pip install \
  ./benchmarks/chemistry-bench-proto ./benchmarks/chemistry-bench-sim
CHEMISTRY_BENCH_SIM_GPU=0 CHEMISTRY_BENCH_FRANKA_USD="$FRANKA_USD" \
  "$ISAAC_PYTHON" -m chemistry_bench_sim.worker --port 50061 \
  --record-dir "$PWD/runs/chemistry-model/continuous" \
  --kit-args --portable-root "$PWD/runs/chemistry-model/kit-cache"
```

`ISAAC_PYTHON` 指向 Isaac 的 `python.sh`，`FRANKA_USD` 指向机器人资产。
选择显存充足的 GPU，确保 Kit 与 CUDA 编号一致。在已测试的多 GPU 服务器上，
GPU 0 配合 `CUDA_VISIBLE_DEVICES=0` 能避免耗时的跨卡检查。无认证的本机 worker
应由当前回合独占；服务启动和受许可资产的准备由操作者完成。

## 运行模型

在另一个终端从仓库根目录执行：

```bash
.venv/bin/python scripts/smoke_chemistry_bench.py \
  --address 127.0.0.1:50061 --output runs/chemistry-model/runtime \
  --agent-config configs/agents/chemistry_bench_titration.yaml \
  --base-url http://127.0.0.1:28000 --episodes 1 --rpc-timeout 600 \
  --timeout-seconds 3600
```

必须传入 `--agent-config`；省略时入口使用固定脚本。模型模式下，每次选择的技能
实际转换为 RPC 原语，动作后重新获得相机图像并验证。私有 pH 和体积只用于评分。
原生成功要求烧杯呈粉红色且已记录现象；归位是指令要求，不额外计入成功条件。
模型自行声称完成不能建立成功。

运行配置通过归一化坐标 `detail_crop` 指定这个固定相机的烧杯区域。模型同时获得
当前完整画面和该区域的 512×512 放大图，录像保留完整场景。局部图仅使用 RGB
像素，没有目标跟踪或颜色合成；改变相机或布局后应调整或关闭裁剪。smoke 入口
读取同一份配置，并开放共享 GPU 上的壁钟时限。早期仅使用全景的失败尝试保留在
验证记录中，不作为成功演示计数。

证据包含 `smoke_summary.json`、`agent_trace.jsonl`、Runtime 视频和 worker 连续视频。
连续视频使用仿真时间，省略模型推理等待。失败尝试保留；RPC 超时会使客户端失效，
应先核对或重启当前专属 worker，再发起新回合。

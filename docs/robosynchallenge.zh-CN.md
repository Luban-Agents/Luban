[English](robosynchallenge.md) · [简体中文](robosynchallenge.zh-CN.md)

# RoboSynChallenge

该接口通过 Luban 的运行、执行与验证流程接入 RoboSynChallenge，支持任务专用 ACT/DP 策略、显式种子、单任务运行和矩阵续跑。RoboSynChallenge 是实验室操作基准，化学滴定视频使用独立的 Isaac Sim 场景。

## 环境与资源

在独立 Python 3.11 仿真环境中，按 [RoboSynChallenge](https://github.com/EDEM-AI/RoboSynChallenge) 与 [EmbodiChain](https://github.com/DexForce/EmbodiChain) 的说明准备 SDK、DexSim、LeRobot、NVIDIA 驱动与任务资产，再安装 Luban。对应参考版本为 RoboSynChallenge `8818c82df5fa2522809b8105e7018950dcc9a9a8`、EmbodiChain `89c14da8d0221dc4ee2a4a3e0ba1078b16d447bd`。模型权重使用与任务一致的公开 ACT 或 DP checkpoint。

## 单权重策略基线

从仓库根目录执行，将三处资源路径替换为本机安装位置。

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

不指定 agent config 时，这是确定性的 `TaskSkillPlanner` / `EnvironmentVerifier` 策略基线。加入 `--agent-config configs/agents/robosynchallenge_act_visual.yaml` 可围绕命令行选择的权重启用视觉规划与验证；由模型选择控制器应使用下方目录模式。先设置 `LUBAN_LLM_BASE_URL`、`LUBAN_LLM_MODEL`，并准备支持图像和结构化输出的模型服务。ACT/DP 不读取规划器的语言指令。

## 模型选择策略目录

智能体实跑使用 `robosynchallenge_act_catalog.yaml`。模型根据任务指令和相机图像，
从全部十种任务控制器中选择一个；该选择实际决定加载哪份 ACT 权重。环境不会按
任务标签将目录限制为单个技能。同一次执行的重试会清空 ACT 动作队列；同技能的
正常重规划保持队列。每个动作记录 `policy_selection`，包含权重和重置原因。
示例使用 1024 token 的回复预算，并要求简洁规划，避免旧 512 token 上限截断回复。
ACT 接收图像和关节状态，子任务文字不直接控制底层运动。此处实现的是任务级技能
调度和视觉监督，没有引入语言条件策略或重新训练阶段控制器。

将十份公开 `ACT_sim_*` 目录放到 `LUBAN_ROBOSYN_MODEL_ROOT` 下，从仓库根目录
使用已准备好的仿真 Python 运行：

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

自带矩阵覆盖十项任务、种子 0–2，共 **30 个新回合**。它用于功能评测，与历史
1000 回合成绩独立。完整评测可将清单中的种子改成所需的全部列表。

```bash
python scripts/eval_robosynchallenge.py \
  --robosyn-root /path/to/RoboSynChallenge \
  --embodichain-root /path/to/EmbodiChain \
  --matrix-manifest configs/runs/robosynchallenge_act_catalog_random.json \
  --matrix-gpus 0 --matrix-scheduling dynamic --record-video \
  --output runs/robosyn-catalog-random
```

## 输出与续跑

输出目录保存 `metadata.json`、`summary.json`、`episodes.jsonl` 及每次尝试的独立记录。成功由环境原生信号判定，执行异常单列。相同设置下增加 `--resume` 跳过已有有效结局，重跑异常或中断回合。改变任务或设置时使用新的进程和输出目录。

矩阵入口为 `--matrix-manifest`，清单包含 `tasks`、`seeds`、`setting` 和 `policy`。单权重模式每项写入 `name` 与 `checkpoint_path`；目录模式使用 `name` 和共享 `agent_config`。使用 `--matrix-gpus` 指定队列，`--matrix-scheduling dynamic` 按空闲 GPU 分配任务。CPU 回归覆盖策略调度、重试、原生结果优先级、种子计数、异常保存和续跑，不启动实际仿真。历史 412/1000 的基准结果见[结果说明](reported-results.zh-CN.md)。

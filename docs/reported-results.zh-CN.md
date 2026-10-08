[English](reported-results.md) · [简体中文](reported-results.zh-CN.md)

# 汇报结果

以下来自现有项目展示页与用户提供的报告记录，属于更大研究项目，不是本包新增评测。
README 的 Leaderboard 为汇报表，不是独立维护的排行榜。

## RoboCasa365 · XR-1

| 设置 | Composite seen 成功率 | Atomic seen 成功率 |
| --- | ---: | ---: |
| XR-1 基线 | 57.1% | 80.2% |
| 无自进化 | 65.0% | 82.1% |
| 有自进化 | 68.6% | 85.5% |

来源为展示页 `results.html`、`js/i18n.js` 与 README 报告说明，Atomic seen 基线于源文件
2026-10-06 更正。有自进化相对无自进化的报告差值：Composite seen +3.6 个百分点，
Atomic seen +3.4 个百分点。

已有摘要未提供这三组 RoboCasa 的任务／回合数、seed 或统计检验，不从其他历史实验推填，
也不新增 unseen 结果。

## LIBERO · OpenVLA-OFT

统一使用 **Without Agent** 与 **Agent**。四个套件、40 个任务，每任务 50 个原始回合 ID，
seed 7，各套件使用对应 OpenVLA-OFT 微调权重。原始对比集共 2,000 个回合 ID。

| 套件 | Without Agent | Agent |
| --- | ---: | ---: |
| libero_goal | 98.4% | 99.4% |
| libero_spatial | 97.6% | 99.4% |
| libero_object | 97.4% | 99.2% |
| libero_10 | 93.4% | 97.6% |
| **整体** | **96.7%** | **98.9%** |

### 指标定义与执行预算

每个原始回合 ID 至少有一条成功执行记录则计为 1，否则计为 0；总和除以原始 ID 数。
同一 ID 在分子中最多计一次。

| 套件 | 原始 ID 数 | Without Agent：完成 ID 数 | Agent：完成 ID 数 |
| --- | ---: | ---: | ---: |
| libero_goal | 500 | 492 | 497 |
| libero_spatial | 500 | 488 | 497 |
| libero_object | 500 | 487 | 496 |
| libero_10 | 500 | 467 | 488 |
| **整体** | **2,000** | **1,934** | **1,978** |

Without Agent 为 1,934 / 2,000 = 96.7%，基于 2,000 次执行。
Agent 为 1,978 / 2,000 = 98.9%，基于原报告的 2,066 次执行。
两列执行预算不同，不建立等预算单次执行对比，也不代表本包的新独立实验。

来源为展示页 `results.html` 与 2026-10-04 报告记录
`assets/evidence/libero-oft-replay-20261004.json`，保留原值及底层计数。
项目来源：[项目展示页](https://github.com/yuliu-ai/OmniRoboAgent-Page)。
本包 GPU 运行入口见[回合指南](episodes.zh-CN.md)。

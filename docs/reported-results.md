# Reported results / 汇报结果

These figures reproduce the existing OmniRoboAgent-Page presentation and its
user-supplied report records. They describe the broader research project rather
than a newly run evaluation of the independent Luban package. The README's
Leaderboard is a report table, not an independently maintained benchmark ranking.

## RoboCasa365 · XR-1

| Setting | Composite seen success | Atomic seen success |
| --- | ---: | ---: |
| XR-1 baseline | 57.1% | 80.2% |
| Framework without self-evolution | 65.0% | 82.1% |
| Framework with self-evolution | 68.6% | 85.5% |

Source: presentation `results.html`, `js/i18n.js` and README report notes;
atomic-seen baseline corrected in that source on 2026-10-06. Self-evolution changes
reported composite-seen success by +3.6 percentage points and atomic-seen success
by +3.4 percentage points relative to the no-evolution setting.

The supplied summary does not give the task/episode counts, seeds or statistical
tests for these three RoboCasa settings. Those details are not inferred from other
historical campaigns. No unseen result is added.

## LIBERO · OpenVLA-OFT

The report compares **Without Agent** and **Agent**, using four suites, 40 tasks,
50 original episode IDs per task, seed 7 and suite-specific OpenVLA-OFT weights.
The original comparison set contains 2,000 episode IDs.

| Suite | Without Agent | Agent |
| --- | ---: | ---: |
| libero_goal | 98.4% | 99.4% |
| libero_spatial | 97.6% | 99.4% |
| libero_object | 97.4% | 99.2% |
| libero_10 | 93.4% | 97.6% |
| **Overall** | **96.7%** | **98.9%** |

### Metric definition and execution budget

For each original episode ID, assign 1 if at least one execution record associated
with that ID has a successful outcome, otherwise 0. Divide the sum by the number
of original episode IDs. Each ID contributes at most once to the numerator.

| Suite | Original episode IDs | Without Agent: completed IDs | Agent: completed IDs |
| --- | ---: | ---: | ---: |
| libero_goal | 500 | 492 | 497 |
| libero_spatial | 500 | 488 | 497 |
| libero_object | 500 | 487 | 496 |
| libero_10 | 500 | 467 | 488 |
| **Overall** | **2,000** | **1,934** | **1,978** |

Without Agent: 1,934 / 2,000 = 96.7%, based on 2,000 executions.
Agent: 1,978 / 2,000 = 98.9%, based on 2,066 executions in the supplied report.
The two columns therefore use different execution budgets. These values do not
establish an equal-budget, single-execution comparison or a new independent run
of this package.

Source: the presentation's `results.html` and its 2026-10-04 report record,
`assets/evidence/libero-oft-replay-20261004.json`. The report values and their
underlying counts are retained; no new experiment is inferred.

## 中文口径

README 汇报表沿用现有前端的项目结果。LIBERO 的对比名称统一为
**Without Agent** 与 **Agent**，按原始 2,000 个回合 ID 统计：每个 ID 至少有一条
成功执行记录则计为 1，否则计为 0，同一 ID 在分子中最多计一次。

Without Agent 为 1,934 / 2,000 = 96.7%，对应 2,000 次执行；
Agent 为 1,978 / 2,000 = 98.9%，对应报告中的 2,066 次执行。
两列执行预算不同，不能据此声称等预算下的单次执行成功率对比。
RoboCasa 的两列保持其任务成功率定义，缺失的实验信息不自行补造。

Project source: [OmniRoboAgent-Page](https://github.com/yuliu-ai/OmniRoboAgent-Page).
This package's runnable GPU entry is the [episode guide](episodes.md).

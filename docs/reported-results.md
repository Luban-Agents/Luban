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

Source: presentation `assets/evidence/libero-oft-replay-20261004.json`, a record of
user-supplied report results. Four suites,
40 tasks, 50 episodes per task, seed 7, 2,000 episodes; suite-specific
OpenVLA-OFT fine-tuned weights.

| Suite | only-VLA | Luban_agent |
| --- | ---: | ---: |
| libero_goal | 98.4% | 99.4% |
| libero_spatial | 97.6% | 99.4% |
| libero_object | 97.4% | 99.2% |
| libero_10 | 93.4% | 97.6% |

Overall: 96.7% for only-VLA and 98.9% for Luban_agent across the 2,000 episodes.

## 中文口径

README 汇报表沿用现有前端的项目结果，不把历史研究结果当作本安装包的新评测。
RoboCasa 的两列均为任务成功率；LIBERO 的两列分别为 only-VLA 与 Luban_agent
在相同 2,000 个回合上的成功率。任务预算、版本与统计信息缺失时不自行补造。

Project source: [OmniRoboAgent-Page](https://github.com/yuliu-ai/OmniRoboAgent-Page).
This package's runnable GPU entry is the [episode guide](episodes.md).

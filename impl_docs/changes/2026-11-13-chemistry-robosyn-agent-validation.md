# Chemistry and RoboSyn agent validation

Status: DONE; both modules verified with live model calls on the current tree.
Base: `2942a6862437aff372a522be8c805bdfdc9f2104`.

## Changes

- RoboSyn supports an explicit skill/checkpoint catalog. Planner output determines
  controller dispatch; task labels do not preselect a checkpoint in catalog mode.
- Retry clears queued ACT actions. Same-skill semantic replanning preserves the
  queue. Unknown skills fail without selecting a fallback controller.
- Actions persist `policy_selection`; evaluation metadata records the catalog's
  checkpoint hashes and source hashes. Single-checkpoint operation remains available.
- Normalize `env_info.success` to the authoritative scalar boolean. The first live
  run exposed that a Tensor trace summary made the new Pipeline report failure
  despite native success. A regression now checks saved Runtime success as well.
- Added a ten-task, seeds 0–2 catalog matrix, bilingual run instructions and a
  model-driven Chemistry guide. Chemistry's fixed scene and grading are unchanged.
- The first Chemistry model attempt reached pink, returned the bottle, then entered
  a repeated-grasp loop and failed after 18 steps / 10 invalid actions. Clarified
  current-image priority, holding-state inference and return/record instructions;
  bounded duplicated memory text. No scripted planner or privileged state was added.
- The second full-frame attempt timed out after 16 primitives. Add an optional
  normalized RGB detail crop for the fixed beaker region, preserving the full
  camera view and video. The smoke runner reads the run-config crop and exposes a
  3,600-second wall-clock budget. Tests verify RGB-only derivation and invalid bounds.
- A RoboSyn planning response exceeded its 512-token cap during the preflight.
  The final catalog config uses concise planning fields and 1,024-token caps for
  planning and visual verification. Earlier runs are not mixed into its results.

## Verification

- RoboSyn adapter/evaluator: 50 tests passed, including different selected
  controllers producing different actions from the same observation and retry reset.
- Final related suite: 184 passed, one optional OpenPI skip. The local gRPC test
  initially could not bind inside the sandbox and passed with loopback enabled.
- Ruff lint/format, mypy for four changed source modules, CLI help and Markdown
  targets/bilingual code blocks passed (360 pages).
- New locked Python 3.11 client environments import this checkout's `luban` package.
  The simulation client reuses existing optional simulation/policy packages read-only
  after the new framework dependencies; previous framework environments are unchanged.

## Live validation

Dedicated final output directories: `runs/chemistry-model-20261113/runtime-v3/` and
`runs/robosyn-agent-validation-20261113/`. No previous rollouts are resumed. Runs use
Qwen3.5-9B, released ACT weights and the pinned RoboSyn/EmbodiChain SDK revisions.
The multi-GPU Isaac startup stalled during peer validation and was stopped; the
replacement uses the previously verified GPU 0 mask. Other processes were not
stopped. The earlier `runs/robosyn-catalog-20261113/` run was stopped after finding
the Tensor/scalar success mismatch; its diagnostics are retained and excluded from
the final evaluation. The `-v2` RoboSyn diagnostics retain the response-cap failure;
the `-v3` startup was replaced before rollouts to use four available GPU queues.
Chemistry's initial config is archived with its source hash; a separate provenance
file identifies each revised config/source snapshot.

Final Chemistry: 14 real model-selected primitives, native success, zero invalid
actions, 1,674.57 seconds wall time. Sequence: pick, eleven 5 mL pours, place,
record. Video `continuous/demo-8b791930b383.mp4` has 1,208 frames at 20 FPS,
60.4 simulation seconds, 1280×832; initial/manipulation/final frames were inspected.

Final RoboSyn: 9/30 successes (30.0%), zero execution/process errors, complete=true.
All ten tasks contain seeds 0–2; all processes and matrix exited 0. Terminations:
9 task_success, 19 environment_done, 2 execution_aborted for uncertainty budget.
Agent audit: 204 live planner calls, 179 visual verifier calls, 12,426 controller
actions, 14 skill switches, no missing artifacts or selection/outcome mismatches.
Current source hashes and the shared agent-config hash match all ten task metadata
files. This is a small functional evaluation, not a rerun of the historical 1000
episodes or evidence of an improvement over ACT.

The dedicated Isaac worker and Qwen service were stopped after their runs. Other
processes and environments were left intact. Results and portable hashes are linked
from the bilingual validation record; large traces/videos remain in ignored runs.

## Pre-push CI

`bash scripts/ci.sh` passed: 1,016 tests passed, 13 optional-dependency skips;
global Ruff lint/format and strict mypy for 169 source files passed. All 37
configuration constructors had zero hard failures; documentation and both catalog
versions passed. Source and wheel distributions built successfully. This check
did not start new GPU rollouts.

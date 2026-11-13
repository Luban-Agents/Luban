# Chemistry and RoboSyn agent validation

Base: Luban `2942a6862437aff372a522be8c805bdfdc9f2104`.
Status: DONE.

## Scope

Validate our existing modules using this checkout, live model calls and new output
directories. Historical parent-project scores and scripted videos are not new
acceptance evidence. Reuse local SDKs, checkpoints and model weights; record their
identity without modifying other users' processes or installations.

## Tasks

- Run the articulated Chemistry scene with its model-configured planner, recording
  actual selected primitives, images, native task feedback and video.
- Retain the existing RoboSyn single-checkpoint baseline. Add an explicit agent
  policy-catalog mode: the planner selects among configured task policies, its
  selection determines the loaded checkpoint, and retry clears queued ACT actions.
  Do not claim that ACT consumes natural-language subtasks.
- Record controller selection in action traces, test dispatch and retry semantics,
  and verify native success remains authoritative.
- Execute a fresh multi-task RoboSyn evaluation with explicit seeds. Report its
  actual coverage and errors separately from historical 1,000-episode results.
- Update bilingual module instructions, current validation evidence and change log.

## Acceptance

Imports resolve to `src/luban` in this checkout. The chemistry demo uses a real
model, not ScriptedPlanner. RoboSyn planner output selects the executed policy;
different selected skills dispatch different checkpoints, and a retry changes
policy state. Saved traces include live planning, verification, actions and native
outcomes. Evaluation failures remain failures; no ground-truth success overrides,
expert action injection or reuse of historical rollouts.

## Completed verification

- Chemistry: real Qwen3.5-9B decisions completed 14 primitives with zero invalid
  actions and native success; the full-scene continuous video is 60.4 simulation
  seconds. Two earlier full-frame failures are preserved. A fixed RGB beaker detail
  view improves readability without exposing grading state.
- RoboSyn: all ten tasks, seeds 0–2, completed afresh: 9/30 successes (30.0%), zero
  execution errors and zero process errors. All task processes and matrix exited 0.
- Evidence: 204 live planning calls, 179 visual verifier calls, 12,426 action chunks
  and 14 real controller switches. Saved Runtime/native outcomes and model-selected
  skills/controller dispatch agree; all final episodes share a source/config identity.
- Related checks: 184 passed, one optional skip; Ruff, four-module strict mypy,
  documentation and source-identity checks passed. Large artifacts remain ignored;
  portable evidence is under `docs/assets/validation/`.

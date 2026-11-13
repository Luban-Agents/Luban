# Luban architecture

This document describes the actual independent snapshot. Current acceptance
evidence belongs in docs/validation.md; parent-project evaluation numbers do not
establish results for this tree.

## Dependency direction

CLI/config composition → Runtime → Pipeline → Agent contracts / Environment contract.
Agent Core → Planner / Verifier / Memory / SkillBackend / LLMBackend contracts.
Concrete benchmark environments → Environment contract and their optional SDKs.
Benchmark evaluators → Runtime/Pipeline/Agent and concrete environment adapters.
ROS2 transport adapters → framework contracts. Core cannot import ROS2, simulator,
evaluation or model SDK implementations. Optional SDK imports remain at use sites.

## Responsibilities

- `agent_core/agents`: `BaseAgent` owns components and client lifecycle;
  `DefaultAgent` delegates and `SelfEvolvingAgent` adds evidence/graph modules.
  Agents do not own or bypass the Pipeline/Environment execution sequence.
- `agent_core/planners`: select task/skill/subtask, optionally use LLM and graphs;
  planners cannot declare benchmark success.
- `backends/skills`: generate open action payloads; no environment execution.
- `environments/base.py`: reset(task), execute(action, execute_steps), close().
  Concrete adapters check payloads and provide authoritative feedback.
- `agent_core/verifiers`: interpret action/environment/visual evidence.
- `pipelines`: call components and maintain explicit deterministic transition state.
  `DirectPipeline` is a closed loop; skill-execution pipelines track executions,
  attempts, budgets, recovery and graph state. `PolicyOnlyPipeline` explicitly
  omits planner/semantic verifier and is not the acceptance example.
- `runtimes`: session creation, limits, scheduling, trace, errors and cleanup;
  no planning policy. Runtime owns mutable state with task/observation/step.
- `observability`: optional compact trace, FFmpeg video and artifact manifest;
  recorder errors do not replace episode outcome.
- `evals/benchmarks`: task enumeration and aggregation, independent of core.

## Contracts and lifecycle

Payloads are ordinary dictionaries/strings/arrays with validation at use sites;
there is no universal Action class or global verifier decision enum. Execute then
observe/verify before the next action. Environment success overrides model claims.
`executed_steps` must be nonnegative integral, progress finite. Runtime records an
explicit reason for each completed session and refuses existing/unsafe session IDs.
KeyboardInterrupt is recorded when possible, resources close, interruption propagates.

Memory holds facts/events and contributes explicit context. Evidence-gated candidate
and experience modules retain their tests but are not evidence of improved task
performance. ModuleEvolutionManager uses one reentrant instance lock for lifecycle
read/transition/append and commit-time paired-evidence rechecks. Separate managers
or processes must not share a writable ledger. Module advisory input reuses the
episode-update step and memory summaries, with the last 12 execution events.
It does not repeat raw model responses or working frames, and does not mutate
the original trace/memory. Proposal-only mode does not apply candidates.

## Configuration and package boundary

Agent YAML composes agent components. Run YAML chooses agent, Pipeline, Runtime,
Environment and task/evaluator. Nested `class_path` construction remains explicit;
stable backend names are a small registry, with no discovery/plugin hierarchy.
Owner-relative agent config paths take precedence; other component paths keep
constructor/CWD semantics. YAML supports environment variables and explicit defaults.

Installed packages are `luban`, `omni_atomic_skills` and the Chemistry
protobuf client. The wheel includes typed markers, Chemistry YAML and the CPU module
example; source archive includes the repository's small configs/catalogs/tests/scripts.
External SDKs, model weights, assets, copied SpatialLM and standalone robot workspaces
are excluded. Upstream Apache-2.0 attribution remains; third-party terms are separate.

RoboCasa applies its process-local EGL context lifecycle guard from `_rendering.py`;
it does not patch shared SDK files. External HTTP/ZeroMQ/WebSocket clients close
connections only. Service startup/shutdown remains an operator action.

## Validation boundary

The supported acceptance path is a CPU mock counter and one real RoboCasa/XR-1
simple task. LIBERO, RoboTwin, EB-ALFRED, Chemistry, OpenPI and experimental spatial,
graph/evolution modules have source/contracts and varying optional test coverage;
no new complete live matrix is claimed. ROS2 has injected transport contracts,
not a verified physical robot installation. General async runtime and physical
robot validation remain unimplemented/unverified scope, respectively.


## Package identity and bilingual guides

The distribution, import namespace and CLI are `luban`; implementation lives under
`src/luban`. Config class paths and owned environment-variable prefixes follow
that identity, including `LUBAN_ROBOCASA_ROOT`. The standalone atomic-skill and
Chemistry protocol packages retain their separate boundaries. No legacy runtime
alias is advertised. Required upstream/source attribution remains accurate.

User guides have complete English/Chinese pairs, linked from docs/README.md and
docs/README.zh-CN.md. The documentation check validates counterparts and identical
executable code blocks. This does not change module ownership or dependency direction.

## RoboSynChallenge integration

The optional RoboSynChallenge environment adapter executes native actions and exposes authoritative task success. Its ACT/DP skill backend generates actions without importing simulator SDKs into core. The evaluator owns explicit seed accounting, result persistence and resume checks. Matrix orchestration belongs under evals, outside Runtime and Agent Core. SDK and policy imports are deferred until use. Git provenance is recorded when available and remains null for source archives or installed packages without checkout metadata.

The policy backend supports a fixed checkpoint and an explicit skill-to-checkpoint
catalog. Catalog mode exposes all configured skills; Planner output selects the
loaded controller. A retry within the same execution resets queued policy actions;
ordinary replanning with the same skill preserves them. ACT/DP remains conditioned
on images and joint state, not the planner's subtask text. Action traces identify the
selected checkpoint and reset reason. The CLI records catalog hashes and executing
source hashes; catalog matrices do not need per-task checkpoint arguments.

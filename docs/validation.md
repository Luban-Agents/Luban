[English](validation.md) · [简体中文](validation.zh-CN.md)

# Validation record

Preparation: 2026-10-07–08. These results were obtained from this independently
prepared current source tree. Parent-project tests and historical catalog probes
are not acceptance results for this copy. The repository remains Private.

## Software checks

| Check | Actual result |
| --- | --- |
| New isolated Python 3.11.16 environment, new dependency cache | installed all declared extras, dev/docs and full-test groups |
| Complete CPU pytest suite | **973 passed, 0 skipped, 0 failures** |
| Independent source-archive environment, no Git metadata | **973 passed, 0 skipped, 0 failures** |
| Earlier core-only/dev environments | 956 passed / 14 optional skips; full group above removes those skips |
| Ruff lint and format | passed |
| Strict mypy | passed; 163 source files |
| Configuration constructors | 35 configs, 0 hard failures; optional service needs are labeled |
| All bundled Markdown targets | passed, including root, catalogs, configs, user/developer guides and HTML links |
| MkDocs strict build | passed |
| V2.1 catalog and bundles | 7236/7236 and 3862/3862 checks passed |
| V2.2 catalog and bundles | 7418/7418 and 3944/3944 checks passed |
| Core module, YAML CLI run and health | passed; two local mock counter actions |
| Wheel install outside source checkout | imports, CLI, typed markers, Chemistry YAML/protobuf and offline module passed |
| Source archive build/install/resources | passed; all CPU tests and bundled examples executed |
| Locked public-index vulnerability metadata | 95 exact package versions queried through official PyPI API, 0 findings |
| Candidate credential scan | supplied-key exact match 0; Gitleaks 33 public sam3_perception route-ID false positives reviewed |
| Current candidate private paths / large files | 0 operational private absolute paths, 0 files above 10 MiB |
| Historical PNG fixtures | 42 simulator images/masks reviewed; public redistribution conditions remain in THIRD_PARTY_NOTICES |
| Existing private baseline CI | `ef4a45c`: fresh Ubuntu runner passed 973 tests plus 973 source-archive tests, no skips; [recorded run](https://github.com/yuliu-ai/final-agent-github/actions/runs/37719142715) |
| Organization repository CI | `04c5e4b`: **973 passed + 973 source-archive tests passed**, zero skips; [recorded run](https://github.com/Luban-Agents/Luban/actions/runs/37723603285). See [Actions](https://github.com/Luban-Agents/Luban/actions) for later exact-commit status |

The test-only group supplies h5py 3.16.0 and Torch 2.14.1+cpu; Dashboard used Gradio
6.28.0. Optional OpenPI tests used the pinned real SDK against local WebSocket
peers. Chemistry uses a local gRPC test peer. These are software/protocol checks,
not live simulator or policy evaluations.

Core versions: httpx 0.28.1, AnyIO 4.15.1, NumPy 1.26.4, Pillow 12.3.0,
PyYAML 6.0.3, pytest 9.1.1, Ruff 0.15.21, mypy 1.20.2, grpcio 1.83.0,
protobuf 7.35.1, pyzmq 27.1.0, msgpack 1.2.1 and MkDocs 1.6.1. The lock is the
installable dependency source. No shared Python environment was changed.

The first follow-up pip-audit request timed out on the network. Every locked
public-index version was then queried successfully against official PyPI
vulnerability metadata; the earlier 90-package pip-audit pass is retained as
separate evidence. This covers database metadata, not the root project, pinned
OpenPI source, CPU binary build, model weights or the reused external GPU stack.
It does not establish absence of vulnerabilities.

An HTTP proxy initially intercepted two loopback WebSocket tests. Setting
`NO_PROXY=localhost,127.0.0.1,::1` resolved both; the complete suite passed again.
The catalog check runs in a temporary copy so historical reports are not rewritten.
The source distribution contains small catalog/evidence resources, policy documents
and the original README SVG; no virtual environment, service credential, weight or
dataset is bundled. The first hosted run found FFmpeg missing before tests; the
workflow now installs it inside the disposable runner. Run
[37675885981](https://github.com/yuliu-ai/final-agent-github/actions/runs/37675885981)
then passed the complete fresh-runner procedure. The source-archive resource check
now explicitly asserts the conduct, contribution, security and license documents.

## Real simulation A: native task with XR-1

Configs: `configs/runs/robocasa_simple.yaml` and `configs/agents/xr1_simple.yaml`.
Task `CloseBlenderLid`, target split, index 0, native reset seed 7, horizon/budget
600 environment steps, at most 38 action chunks / 40 iterations / 600 seconds,
receding horizon 16. A deterministic TaskSkillPlanner selects the native instruction;
XR-1 generates real actions and EnvironmentVerifier reads native success. No LLM
is used in this example.

```json
{
  "success": true,
  "termination_reason": "task_success",
  "environment_steps": 396,
  "action_chunks": 25,
  "exceptions": 0
}
```

Session `5d67f5f7-d749-440f-98de-899082e812f8`, under
`runs/robocasa_simple/<session_id>/`. Result, both traces, manifest and video were
produced; the video decoded completely and its first three-view frame was inspected.
See [reproduction commands](episodes.md).

## Real simulation B: multimodal graph-guided agent

Configs: `configs/runs/robocasa_graph_simple.yaml` and
`configs/agents/xr1_graph_simple.yaml`. Task `ScrubCuttingBoard`, target split,
index 0, native reset seed 7, 600 environment-step horizon/budget, at most 38 chunks,
80 iterations and 600 seconds. XR-1 service uses task_graph instruction mode and
GLM-5.3-flash supplies real image/JSON planning and verification calls.

```json
{
  "success": false,
  "termination_reason": "environment_done",
  "environment_steps": 600,
  "action_chunks": 38,
  "planner_calls": 2,
  "verifier_calls": 3,
  "exceptions": 0
}
```

Two real executions used the same task/seed/bounds. They both reached the native
600-step horizon without completing the task; each had two planner calls, three
verifier calls, 38 chunks and zero Runtime exceptions.

| Session | Wall time | Post-episode processing |
| --- | --- | --- |
| `7e6adb49-5182-4089-a731-0496f78a14e8` | 233.48 s | Initial 4096-token reflection and advice were truncated (`finish_reason=length`); two update errors |
| `ab2b88f1-80a3-43a6-9d90-790f572fd7f9` | 345.98 s | 16384-token reflection passed; module advice hit its then-120-second read deadline; one update error |

Sessions are under `runs/robocasa_graph_simple/traces/<session_id>/`. The first
contains 199 runtime trace records, 38 memory-update events, a one-node
catalog-validated task graph in planner inputs, a finalized manifest and 39-frame
video. Runtime exceptions and post-update errors are separate fields: zero of the
former does not mean every reasoning stage passed. Neither run applied a high-skill
or module update. The later run retained one reflection proposal, one experience
candidate and a deterministic fallback module candidate.

The final code sends compact existing step/memory summaries to module advice,
retaining the last 12 events, feedback and artifact references while leaving the
original trace intact. A separate live advisory check used the second session's
recorded evidence: one GLM-5.3-flash request, 12431-byte input, 16384-token cap,
300-second deadline, 79.11 seconds elapsed, 13262 total tokens. It parsed four
proposals and accepted four proposal-only candidates, applying zero changes and
executing zero new environment steps. This passed advisory check is not a rerun
of the robot episode or evidence of task improvement. The current full 300-second
post-processing configuration has not been rerun end to end; the component check
and the real episode remain separately reported.

This is the existing graph-guided compatibility path: selective node scheduling /
recovery is disabled, and each result's task_graph_runtime is null. The trace proves
real graph context, model/policy calls and feedback/memory updates, not a separately
validated node-scheduler deployment. No successful experience promotion, weight
training, cross-robot transfer or policy improvement is claimed. The first attempt
with CloseBlenderLid stopped before actions because the default composite-task
catalog does not bind it; the documented entry uses the existing ScrubCuttingBoard
binding. See [advanced reproduction](advanced-episode.md).

## External runtime and verification limits

Both simulation examples reused RoboCasa 1.0.1 source reference
`456174f62b89b8fca99eaaf33949c29fec9cfc2a`, robosuite 1.5.2, MuJoCo 3.3.1,
existing licensed assets and Xiaomi-Robotics-1-RoboCasa365 weights read-only.
The policy source archive has no Git metadata; selected fingerprints are retained
privately, but exact equivalence to the retrieval revision and all shard digests
were not established. Full GPU-stack installation from scratch was not verified.
The policy service used its existing Python 3.12.14 environment; the installed
framework client remains Python 3.11.16. Each acceptance service was independently
started on idle GPU 0 / port 18400 and stopped after its run. Existing shared
services were not restarted or signalled.

A separate live GLM text/mock-counter example passed two planner requests. A
single bounded image/JSON compatibility request also passed (858 total tokens).
Credentials came from a private external environment file into process memory;
no key or real gateway configuration was written into the candidate.

During the October validation, no live LIBERO/OpenPI policy, RoboTwin, EB-ALFRED, Isaac Sim, SAM3/SpatialLM,
physical robot, broad task matrix, long durability run or training was executed.
These remaining live combinations need their own licensed resources and validation.
One native-task success and two horizon failures are not aggregate performance results.

## Private repository and provenance

Selected delivery target: `Luban-Agents/Luban`, a new organization-owned Private
repository. Organization registration, repository creation and normal push are complete. The
API verified Private before and after pushing. A fresh authenticated GitHub clone
installed in an independent core environment and passed both mock examples and
health checks. The organization CI passed all 973 tests plus the 973-test source
archive check at `04c5e4b` (run linked above). The sole owner administers the repository.
The second organization member has explicit repository Read access, with no
push/triage/maintain/admin permissions; organization base permission is None.

The owner selected a new repository rather than replacing the personal repository's
history. Only the reviewed independent preparation history was pushed
to the new repository. Legacy `main` and its ancestors are excluded. The existing
personal repository stays Private as a backup, without transfer or force push.
Its early commits retain historical resource paths/hardware identifiers; those
historical objects are not part of the reviewed preparation branch.

No public Release, Pages, website or visibility change is authorized. Before any
future public release, review the fixture and institutional redistribution
conditions in [third-party notices](../THIRD_PARTY_NOTICES.md). Private account
access and editing instructions are in [Access and editing](access.md).

Raw test/install reports, dependency metadata, scans and runtime outputs remain in
ignored local evidence storage. The original source preservation and final exact
revision/Private receipts are included in the private delivery report. See
[source provenance](provenance.md) and [development](development.md).

## Luban namespace and bilingual guide verification (2026-10-08)

The installable distribution, import namespace and CLI are now `luban`; source
is under `src/luban`. Owned SDK-root variables use `LUBAN_ROBOCASA_ROOT`.
Nineteen complete English/Chinese guide pairs share identical executable code
blocks and paired navigation. The original upstream attribution remains unchanged.

A new isolated environment installed the frozen all-extras/dev/docs/full-test set.
The migrated local suite passed 973 tests with zero skips; lint, formatting, strict
types and 35 configuration constructors passed. The GPU client used the owned
simulator environment reinstalled as Luban, and the policy environment/weights
were reused read-only. GPU 4 and loopback port 18408 were checked before startup.

The migrated real task used the existing CloseBlenderLid target/index 0/seed 7,
600-step, 38-chunk, 600-second configuration. It ended with native task_success,
352 environment steps, 22 chunks and zero exceptions. Session:
`18c04c6f-a2f8-41ae-9bfa-3bef5ff93773` under `runs/robocasa_simple/`.
Both traces, result, artifact manifest and video were produced. The owned policy
service stopped after verification. No shared environment or original source changed.

Independent distribution/resource checks and the final exact-commit GitHub CI are
recorded with this migration's delivery evidence; historical runs above retain
their original dates and identities.

## Chemistry and RoboSyn refresh (2026-11-13)

These checks use Luban base `2942a6862437aff372a522be8c805bdfdc9f2104` plus the
[module validation changes](../impl_docs/changes/2026-11-13-chemistry-robosyn-agent-validation.md).
Executing source/config hashes are retained with the new runs. They do not reuse
parent-project rollout results. Related regression: **184 passed, one optional
OpenPI skip**; Ruff, strict mypy for four changed modules and bilingual Markdown
checks passed. The optional GPU stack and model weights were reused read-only;
new framework dependencies were installed in isolated locked Python 3.11 environments.

### Articulated chemistry demo

The fixed titration completed through `LanguageSkillPlanner`, Qwen3.5-9B,
`LanguageSkillBackend`, `DirectPipeline` and the real Isaac Sim worker. All 14
planner calls identify the live model and select the actual RPC primitive:
pick, eleven 5 mL pours, place and record. Native success is true, Runtime ends
with `task_success`, and invalid actions are zero. Privileged pH/volumes remain
grading-only. The model uses a full frame plus a fixed RGB beaker crop; robot
motion remains scripted Lula IK and chemistry remains symbolic.

| Item | Measured result |
| --- | --- |
| Completed configured smoke | 1 episode, 14 primitives, native success |
| Wall-clock episode time | 1,674.57 seconds on the shared host |
| Continuous video | 1,208 frames, 20 FPS, 60.4 simulation seconds, 1280×832 |
| Earlier full-frame attempts | invalid-action limit after 18 steps; timeout after 16 steps |

The two development failures remain archived and are not evidence of a 100%
success rate. This is one fixed-task functional demonstration. Continuous video
omits model inference pauses; wall time and video length measure different things.
Initial, lifted, pouring and final pink/returned-bottle frames were inspected.

Session: `2f21298a-7aa7-47b4-832c-702a06dd03f0`, under
`runs/chemistry-model-20261113/runtime-v3/`. The continuous clip is
`runs/chemistry-model-20261113/continuous/demo-8b791930b383.mp4`.
Versioned provenance and earlier config/source snapshots accompany those outputs.
See the [chemistry reproduction guide](chemistry.md).

### RoboSyn agent evaluation

Ten official tasks were run with `random` setting and explicit unfiltered seeds
0–2: **9/30 successes (30.0%)**, zero execution exceptions, zero process errors.
All ten task workers and the matrix exited 0; the summary reports `complete=true`.
Nineteen unsuccessful episodes reached environment termination; two sample-loading
episodes ended when the visual verifier's uncertainty budget was exhausted.

| Task | Successes / episodes |
| --- | ---: |
| click_bell | 2 / 3 |
| drawer_open_place | 0 / 3 |
| handle_basket | 0 / 3 |
| item_assembly | 1 / 3 |
| items_handover | 0 / 3 |
| manipulate_pipette | 2 / 3 |
| mixer_operating | 0 / 3 |
| sample_loading | 0 / 3 |
| table_rearrangement | 3 / 3 |
| water_pouring | 1 / 3 |

The configured `DefaultAgent` uses Qwen3.5-9B planning/verification, `TieredMemory`,
`SkillExecutionPipeline` and released task-specific ACT checkpoints. The model sees
all ten skills and chooses the executed controller. The completed traces contain
**204 live planner calls, 179 visual verifier calls, 12,426 action chunks and 14
actual controller switches**. Every recorded action agrees with the planner's
selected skill, and all Runtime/native success flags agree. ACT itself consumes
images and joint state, not the subtask's language. No expert actions or training
were used. This verifies agent-driven task-level dispatch and feedback control;
it is not evidence that subtask prose conditions ACT movements.

Planner and visual verification intervals are 64 chunks, response caps 1,024 tokens,
Runtime bounds 10,000 iterations / 1,800 seconds, and native task horizons remain
active. RoboSyn `8818c82df5fa2522809b8105e7018950dcc9a9a8` and EmbodiChain
`89c14da8d0221dc4ee2a4a3e0ba1078b16d447bd` were clean. The reused simulation stack
is Python 3.11.15, Torch 2.7.1, NumPy 1.26.4, DexSim 0.4.3 and LeRobot 0.3.3.
Four task queues used RTX A6000 GPUs 2/3/4/7; the local Qwen service used GPU 3.
Source and checkpoint hashes are saved; all 30 episodes share one agent-config hash.

This small functional sample is separate from the historical 412/1000 result and
the organizer's expert-filtered evaluation. It cannot establish an improvement
over ACT or any planning/memory contribution without matched baselines and ablations.
Cross-task controller choices appear in failure traces, so routing accuracy also
affects this agent-level result. Earlier signal-normalization and response-cap
preflights remain archived and are excluded from the 30 final episodes.

Outputs: `runs/robosyn-agent-validation-20261113/`; `agent-audit.json` checks the
model/controller chain, success agreement and artifacts. The small portable
[evidence summary](assets/validation/chemistry-robosyn-20261113.json) contains the
results, seeds, source/config/checkpoint hashes and regression counts without local
installation paths. Large videos and complete traces remain outside version control.
See the [RoboSyn run guide](robosynchallenge.md).

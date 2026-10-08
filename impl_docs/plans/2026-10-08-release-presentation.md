# Luban README presentation and GPU onboarding

Status: DONE

## Scope

Refresh the bilingual framework README with original Luban branding and a clear
Project / arXiv / Demo navigation strip. Reuse the existing OmniRoboAgent-Page
frontend. Do not create a second website, publish a site/release, or change repository
visibility. Preserve the frontend's existing uncommitted work.

Improve the existing RoboCasa365 + XR-1 GPU onboarding path without adding a
general asynchronous runtime or physical robot control. CPU and GPU execution
remain distinct supported entry points.

## Implementation

- [x] Original editable SVG mark/wordmark and execution diagram; light/dark headers.
- [x] Bilingual README removes preparation badges, approval banners and validation navigation.
- [x] Project and Demo resolve to the existing frontend guide while hosted URLs are unavailable.
- [x] arXiv explicitly remains unpublished, with no invented identifier.
- [x] New alternative frontend draft preserved outside Git and distributions.
- [x] Fixed official robosuite source avoids the PyPI Mink / NumPy dependency conflict.
- [x] Isolated simulator runtime, GPU/resource preflight and portable service/GPU selection.
- [x] Real bounded CloseBlenderLid episode with existing weights and a temporary owned service.
- [x] Existing frontend static checks; local CPU tests, docs and packaging checks.
- [x] Independent wheel/source installation and archive tests; content and credential review.
- Remote visibility and CI are checked again when pushing the final commit.

## Acceptance evidence

The real fresh-runtime episode completed with task_success, 376 environment steps,
24 action chunks and zero exceptions. The policy environment and checkpoint were
reused read-only, while the simulator runtime and fixed SDK source were independently
installed. This does not claim a fresh CUDA driver installation or broad benchmark
coverage. The existing frontend passed its 12-page / 322-link static check.

Public URLs and the paper identifier are filled in when provided; no hosting is
performed as part of this work. The existing frontend's broader historical results
are not copied into the framework's support claims.

[English](reader-console.md) · [简体中文](reader-console.zh-CN.md)

# Offline replay console

[Open the 2026-10-13 online preview](https://6acda06095d8304cc3c58976--luban-consoles-20261008.netlify.app/offline/). The public presentation contains eight recorded episodes, three camera views, task graphs and Planner/Verifier events. Select a case and start playback, then pause, seek or inspect node details. This entry does not connect model services or execute new robot tasks.

The 2026-10-18 local delivery collects the console and project pages in one website root. `offline/` opens replay. The legacy `expert/` and `reader/` paths show the same offline page. A new deployment can use one domain, while the existing online preview retains its earlier version.

The task graph uses a presentation timeline mapped to video frames. At the environment-success frame, delayed goals can be shown as resolved by the task outcome, retaining original node states and execution records. This separately maintained frontend does not change framework distribution scope. For real execution, follow [installation](installation.md), [configuration](configuration.md) and [episodes](episodes.md).

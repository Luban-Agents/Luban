[English](reader-console.md) · [简体中文](reader-console.zh-CN.md)

# Offline replay console

[Open the replay console (2026-10-20)](https://liutong-luban-demo.netlify.app/). The public presentation contains eight recorded episodes, three camera views, task graphs and Planner/Verifier events. Select a case and start playback, then pause, seek or inspect node details. This entry does not connect model services or execute new robot tasks.

The console uses a dedicated liutong-luban-demo.netlify.app domain and opens directly at its root. Project home returns to liutong-luban-project.netlify.app. Legacy offline/expert/reader links redirect to the current replay entry. Chinese presentation uses 六通智能体 and the English project name is Luban.

The task graph uses a presentation timeline mapped to video frames. At the environment-success frame, delayed goals can be shown as resolved by the task outcome, retaining original node states and execution records. This separately maintained frontend does not change framework distribution scope. For real execution, follow [installation](installation.md), [configuration](configuration.md) and [episodes](episodes.md).

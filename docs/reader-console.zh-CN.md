[English](reader-console.md) · [简体中文](reader-console.zh-CN.md)

# 离线案例演示台

[打开 2026-10-13 在线预览](https://6acda06095d8304cc3c58976--luban-consoles-20261008.netlify.app/offline/)。公开展示提供八个录制回合、三路相机画面、任务图、Planner 与 Verifier 事件。选择案例后点击开始，可暂停、拖动进度和查看节点详情。此入口不连接模型服务，也不执行新的机器人任务。

2026-10-18 本地交付将控制台与项目展示页整理在同一网站目录。`offline/` 是回放入口，`expert/` 与 `reader/` 兼容旧路径并显示同一离线页面。新账号发布后可使用同域名链接，当前线上预览保持原版本。

任务图使用录像帧对应的展示时间轴。环境成功终帧可将记录延迟的目标显示为随任务达成，原始节点状态与执行记录仍保留。控制台是独立维护的前端，框架安装包范围保持不变。自行执行任务请按[安装](installation.zh-CN.md)、[配置](configuration.zh-CN.md)与[回合指南](episodes.zh-CN.md)准备资源。

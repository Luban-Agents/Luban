[English](project-page.md) · [简体中文](project-page.zh-CN.md)

# Project · arXiv · Demo

## Project

[项目展示页](https://liutong-luban-project.netlify.app/)于 2026-10-20 发布，包含项目概览、跨域能力、记忆、自进化、架构、实验结果、原子技能、任务演示与恢复说明。历史网站源码仓库为 [OmniRoboAgent-Page](https://github.com/yuliu-ai/OmniRoboAgent-Page)，与本框架仓库独立维护。

当前网站包含 2026-10-18 新增的空间记忆详解、三个应用场景与最新架构图。项目页与八案例展示页分别使用能体现用途的独立域名，点击展示入口后可从控制台返回项目首页。中文名称统一为六通智能体，英文名称为 Luban。

## Demo

[任务录像](https://liutong-luban-project.netlify.app/demos.html)与[离线案例控制台](https://liutong-luban-demo.netlify.app/)为现有在线入口。网站包含交通机器人、隧道机器狗、公路无人机各 35 秒视频节选，并保留原有任务录像、RoboTwin 与化学测评结果。

从整合后的网站目录预览：

```bash
python3 -m http.server 8118 --bind 127.0.0.1
```

打开 `http://127.0.0.1:8118/` 查看项目首页，打开 `http://127.0.0.1:8118/offline/` 查看回放。交付包提供双击启动入口。只读回放不需要模型、API 或远程机器。

## arXiv

六通智能体 论文尚无已确认的 arXiv 编号。引用见 [CITATION](../CITATION.zh-CN.md)。

## 发布状态

项目首页与案例展示页已分别部署到 liutong-luban-project.netlify.app 和 liutong-luban-demo.netlify.app，双语 README 顶部的 Project、Demo、Offline Replay 链接均已更新。GitHub 仓库继续保留私有权限，受邀协作者登录后可访问。

前端介绍覆盖更大项目的研究与应用素材，具体软件支持范围见[环境指南](environments.zh-CN.md)。

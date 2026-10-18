[English](project-page.md) · [简体中文](project-page.zh-CN.md)

# Project · arXiv · Demo

## Project

[项目展示预览](https://6acd9e44e89af57fccde9564--friendly-hotteok-b5a87f.netlify.app/)对应 2026-10-13 版本，包含项目概览、跨域能力、记忆、自进化、架构、实验结果、原子技能、任务演示与恢复说明。历史网站源码仓库为 [OmniRoboAgent-Page](https://github.com/yuliu-ai/OmniRoboAgent-Page)，与本框架仓库独立维护。

2026-10-18 新增空间记忆详解和三个应用场景，当前保存在统一的本地网站文件夹中。项目展示页与八案例离线控制台共用网站根目录，通过 `offline/index.html` 进入回放，再返回首页。本次 GitHub 更新包含新版说明和架构图。网站部署继续等待新 Netlify 账号就绪。

## Demo

[任务录像](https://6acd9e44e89af57fccde9564--friendly-hotteok-b5a87f.netlify.app/demos.html)与[离线案例控制台](https://6acda06095d8304cc3c58976--luban-consoles-20261008.netlify.app/offline/)为现有在线入口。新本地交付增加交通机器人、隧道机器狗、公路无人机各 35 秒视频节选，并保留原有任务录像、RoboTwin 与化学测评结果。

从整合后的网站目录预览：

```bash
python3 -m http.server 8118 --bind 127.0.0.1
```

打开 `http://127.0.0.1:8118/` 查看项目首页，打开 `http://127.0.0.1:8118/offline/` 查看回放。交付包提供双击启动入口。只读回放不需要模型、API 或远程机器。

## arXiv

六通智能体 论文尚无已确认的 arXiv 编号。引用见 [CITATION](../CITATION.zh-CN.md)。

## 后续发布

在新账号中发布交付包的 `网站/` 目录即可得到同一域名下的项目展示与回放入口。发布成功后再更新双语 README 顶部的 Project、Demo、Offline Replay 链接。当前预览网址保留真实版本日期。

前端介绍覆盖更大项目的研究与应用素材，具体软件支持范围见[环境指南](environments.zh-CN.md)。

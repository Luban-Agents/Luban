[English](project-page.md) · [简体中文](project-page.zh-CN.md)

# Project · arXiv · Demo

Luban 沿用已有项目展示前端。当前仓库提供框架、示例与文档；展示页由独立
[源码仓库](https://github.com/yuliu-ai/OmniRoboAgent-Page)维护。

<a id="project"></a>

## Project

首页为 `index.html`，连接项目概览、跨域能力、记忆、自进化、系统架构、结果、技能、
任务演示与恢复。README 尚未填写正式托管 Project URL；网址提供后直接连接已有首页。

<a id="demo"></a>

## Demo

同一前端目录中的 `demos.html` 提供任务视频与观看说明，还保留恢复、自进化案例。
这些是已录制演示，不是与 GPU 或机器人实时连接。

在已有前端目录中本地预览：

```bash
python3 -m http.server 8092 --bind 127.0.0.1
```

Project 打开 `http://127.0.0.1:8092/`，Demo 打开 `http://127.0.0.1:8092/demos.html`，
Ctrl-C 停止。维护者的前端工作树含未提交编辑，不随框架分发包提供，预览需使用准备好的前端目录。

展示页包含更大研究项目与历史实验；本仓库实际运行范围以[首页](../README.zh-CN.md)、
[安装](installation.zh-CN.md)、[回合配置](episodes.zh-CN.md)为准，展示结果不能自动当成本包的结果。

<a id="arxiv"></a>

## arXiv

**待发布。** Luban 论文尚无 arXiv 编号，这个入口只保留导航位置，不编造链接。
软件归属引用见 [CITATION.md](../CITATION.zh-CN.md)。

## 更新最终链接

英文、中文 README 顶部均有 `project-links` 区块。
网址确认后，将 Project／Demo 替换为已有首页和 `demos.html` 的正式 URL，
arXiv 替换为真实 `https://arxiv.org/abs/...` 地址；之前三个入口均指向本说明。

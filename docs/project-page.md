# Project · arXiv · Demo

Luban uses the existing **OmniRoboAgent-Page** frontend. This code repository
contains the framework, examples and documentation; the presentation website is
maintained in its own [source repository](https://github.com/yuliu-ai/OmniRoboAgent-Page).

## Project

The existing homepage is `index.html`. It links to the project overview, cross-domain
capabilities, memory, self-evolution, architecture, results, skills, task demos
and recovery pages. No hosted Project URL has been assigned to this README yet.
The Project button will point directly to the deployed homepage when its URL is available.

## Demo

Use `demos.html` in the same frontend checkout for task videos and viewing guides.
The website also retains its existing recovery and self-evolution demonstrations.
These are recorded demonstrations, not a live connection to a robot or GPU service.

To preview the existing frontend on your computer, from that frontend's directory:

```bash
python3 -m http.server 8092 --bind 127.0.0.1
```

Open `http://127.0.0.1:8092/` for Project and
`http://127.0.0.1:8092/demos.html` for Demo. Stop with Ctrl-C.
The current maintainer working tree contains frontend edits not yet committed to
its source repository; those edits are not bundled into the framework distribution.
Use the prepared frontend checkout for this preview.

The presentation site covers a broader research project and historical experiments.
For the executable scope of this repository, use its [README](../README.md),
[installation guide](installation.md) and [episode configuration](episodes.md).
Website results are not automatically results of this package version.

## arXiv

**Coming soon / 待发布。** The Luban paper has not been published and has no assigned
arXiv identifier. This entry reserves the navigation position without inventing a
paper link. Software attribution is in [CITATION.md](../CITATION.md).

## Updating the final links

The English and Chinese README files contain a `project-links` block near the top.
Once final URLs exist, replace the Project and Demo destinations with the existing
website homepage and `demos.html`; replace arXiv with the actual paper's
`https://arxiv.org/abs/...` URL. Until then, all three buttons resolve to this page.

## 中文说明

沿用已有 `OmniRoboAgent-Page` 前端：`index.html` 为项目首页，`demos.html` 为任务演示。
现有页面和素材保持原有结构，不在框架仓库另建网站。Project 和 Demo 的正式网址
尚未填入；论文未发布，arXiv 入口暂时说明状态。上面的命令用于已有前端目录的本地预览。

前端展示包含更大研究项目及历史实验，其能力和结果不能直接当作本包的验证结论。
本包安装与 GPU 回合入口以本仓库文档和配置为准。

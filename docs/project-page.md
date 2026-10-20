[English](project-page.md) · [简体中文](project-page.zh-CN.md)

# Project · arXiv · Demo

## Project

The [project website](https://liutong-luban-project.netlify.app/) was published on 2026-10-20. It covers the overview, cross-domain capabilities, memory, evolution, architecture, results, skills, recordings and recovery. The historical [OmniRoboAgent-Page source repository](https://github.com/yuliu-ai/OmniRoboAgent-Page) is maintained separately from this framework repository.

The published website includes the 2026-10-18 spatial-memory details, three application scenarios and latest supplied architecture diagram. The project page and eight-case replay console use separate named domains. Follow the replay link from the project homepage and use Project home in the console to return. Chinese presentation uses 六通智能体, while English presentation uses Luban.

## Demo

Online entries are [task recordings](https://liutong-luban-project.netlify.app/demos.html) and the [offline console](https://liutong-luban-demo.netlify.app/). The website includes a 35-second source excerpt for each of the traffic robot, tunnel quadruped and highway drone scenarios, retaining earlier task recordings and RoboTwin and chemistry results.

Preview from the integrated website directory:

```bash
python3 -m http.server 8118 --bind 127.0.0.1
```

Open `http://127.0.0.1:8118/` for the homepage and `http://127.0.0.1:8118/offline/` for replay. The delivery also includes a double-click launcher. Replay requires no models, API or remote machine.

## arXiv

No arXiv identifier has been confirmed for the Luban paper. See [CITATION](../CITATION.md).

## Publication

The project homepage uses liutong-luban-project.netlify.app and the replay console uses liutong-luban-demo.netlify.app. The Project, Demo and Offline Replay links in both README files point to this deployment. The GitHub repository remains private for invited collaborators.

The frontend includes broader project research and application materials. Package support is defined by the [environment guide](environments.md).

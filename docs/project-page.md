[English](project-page.md) · [简体中文](project-page.zh-CN.md)

# Project · arXiv · Demo

## Project

The [project preview](https://6acd9e44e89af57fccde9564--friendly-hotteok-b5a87f.netlify.app/) is the 2026-10-13 version. It covers the overview, cross-domain capabilities, memory, evolution, architecture, results, skills, recordings and recovery. The historical [OmniRoboAgent-Page source repository](https://github.com/yuliu-ai/OmniRoboAgent-Page) is maintained separately from this framework repository.

The 2026-10-18 update adds spatial-memory details and three application scenarios in a unified local website folder. The project pages and eight-case replay console share a website root. Open `offline/index.html` for replay and return to the homepage from there. The updated documentation and architecture diagram are included in this GitHub revision. Website deployment remains deferred until the new Netlify account is ready.

## Demo

Existing online entries are [task recordings](https://6acd9e44e89af57fccde9564--friendly-hotteok-b5a87f.netlify.app/demos.html) and the [offline console](https://6acda06095d8304cc3c58976--luban-consoles-20261008.netlify.app/offline/). The local delivery adds a 35-second source excerpt for each of the traffic robot, tunnel quadruped and highway drone scenarios, retaining earlier task recordings and RoboTwin and chemistry results.

Preview from the integrated website directory:

```bash
python3 -m http.server 8118 --bind 127.0.0.1
```

Open `http://127.0.0.1:8118/` for the homepage and `http://127.0.0.1:8118/offline/` for replay. The delivery also includes a double-click launcher. Replay requires no models, API or remote machine.

## arXiv

No arXiv identifier has been confirmed for the Luban paper. See [CITATION](../CITATION.md).

## Later publication

Deploy the delivery's `网站/` directory in the new account to host presentation and replay under one domain. After deployment, update the Project, Demo and Offline Replay destinations in both README files. Existing previews retain their actual version date.

The frontend includes broader project research and application materials. Package support is defined by the [environment guide](environments.md).

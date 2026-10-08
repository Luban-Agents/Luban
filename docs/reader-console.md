# Reader Console / 读者操作演示台

**[Open the reader operation console](https://luban-consoles-20261008.netlify.app/reader/)**

This is the existing, separately maintained reader console. The README links to
it without bundling or redeploying its frontend/backend into the framework package.

The console's live workflow needs the reader's own backend, model/policy service
and simulation resources. A static web page does not supply GPU computation.
For framework setup, use [installation](installation.md), [configuration](configuration.md)
and [episodes](episodes.md); follow the console's own connection instructions for
its supported backend and configuration format.

The framework CLI can be used independently of this external page. Publication of
a console link does not change this GitHub repository's visibility or access rights.

## 中文说明

入口沿用已有读者控制台，不在本仓库重新开发或部署一套前端。实际执行需要自行准备
后端服务、策略模型与仿真资源；网页本身不提供公共 GPU。操作台的连接方法与支持的
后台版本以页面说明为准。本仓库提供可独立使用的安装、配置和 CLI 运行路径。

[English](provenance.md) · [简体中文](provenance.zh-CN.md)

# 源码来源与分发边界

本版本基于 2026-10-07 交付的 `Final agent` 实际工作树，来源为 OmniRoboAgent commit
`bc37672c7baa68c50effdb464ee56e2746bd9dae`，并包括当时未提交的分发边界与 RoboCasa
渲染修复。准备输入包含相关现有文件、未提交修改与未跟踪源码／测试。
仓库使用独立历史，不分发父仓库未经审阅的完整 Git 历史。

上游参考：[OmniRoboAgent](https://github.com/choucaicai/OmniRoboAgent)。
当前运行命名空间为 `luban`；Apache-2.0 及原有文件级归属保留。
准备改动见[变更记录](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/impl_docs/changes/2026-10-07-private-github-preparation.md)。
没有为本副本编造作者、论文、DOI 或基准成绩。

包含：框架／原子技能源码、自有 Chemistry 协议与 worker、测试、脚本、配置、小型 JSON／JSONL
catalog 与知识示例、用户／开发文档。知识模板是示例，不是对应研究或跨本体迁移的新增实证。

不纳入 Git／源码分发包：复制的 SpatialLM、独立机器人／导航工作区及厂商 CAD、模型权重、
数据集／大型资产、运行输出、私人凭据、内部运行历史和原始 Git 元数据。
准备机器上忽略的私有保留区不属于交付仓库，也不是安装依赖。

第三方 SDK 通过外部依赖获取，不隐式导入父目录。
来源清单见 [third_party/SOURCES.toml](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/third_party/SOURCES.toml)。
OpenPI 使用固定归档可选依赖。EmbodiedBench 的上游许可证接口未建立再分发许可，
不复制其源码，也不再推荐旧依赖 preset。
完整条件见[第三方声明](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/THIRD_PARTY_NOTICES.md)。

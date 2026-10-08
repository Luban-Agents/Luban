# 访问与编辑 / Access and editing

## 中文

仓库地址为 `Luban-Agents/Luban`，默认分支为 `codex/private-readiness`。
组织所有者负责管理；受邀查看者使用 **Read** 权限。
邀请需由接收方登录自己的 GitHub 账号接受，接受后才能网页查看及 clone。
Read 允许下载和修改自己的本地副本，但不能 push 到本仓库，也不能邀请其他人。

使用已获授权的账号登录 GitHub。HTTPS 用户可以先配置已有认证：

```bash
gh auth login --hostname github.com --git-protocol https
gh auth setup-git --hostname github.com
git clone --branch codex/private-readiness --single-branch https://github.com/Luban-Agents/Luban.git
cd Luban
uv sync --frozen --no-dev --python 3.11
uv run --frozen --no-dev python -m omniroboagent.examples.offline
```

不要把 token 放进 clone URL、YAML 或文档。`Repository not found` 常表示
当前账号未获授权或尚未接受邀请；先检查 `gh auth status` 中的账号。

| 想修改的内容 | 从这里开始 |
| --- | --- |
| 中文项目首页 | [README.zh-CN.md](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/README.zh-CN.md) |
| 英文项目首页 | [README.md](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/README.md) |
| 入门运行步骤 | [quickstart.md](quickstart.md) |
| 真实任务、seed、运行预算和结果目录 | [robocasa_simple.yaml](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/configs/runs/robocasa_simple.yaml) |
| XR-1 策略连接和智能体组件 | [xr1_simple.yaml](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/configs/agents/xr1_simple.yaml) |
| 多模态模型与任务图组件 | [xr1_graph_simple.yaml](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/configs/agents/xr1_graph_simple.yaml) |
| CLI 命令和配置入口 | [cli.py](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/src/omniroboagent/cli.py) |

有写入权限的所有者可在 GitHub 打开文件，点击 **Edit this file**，修改并
**Commit changes**。修改运行代码前先阅读 [开发指南](development.md)、
[项目规则](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/rules/README.md)和[架构](https://github.com/Luban-Agents/Luban/blob/codex/private-readiness/impl_docs/architecture/overview.md)。
模型凭据使用环境变量，按[配置指南](configuration.md)填写，不提交实际密钥。

## English

The repository is `Luban-Agents/Luban`; the default branch is
`codex/private-readiness`. An organization owner administers the repository.
A **Read** invitation lets its recipient browse and clone after accepting it with
the invited GitHub account. Read does not permit pushing to this repository or
managing its access. Recipients can edit their own local copies.

The commands above authenticate with the user's existing GitHub credentials,
clone the reviewed branch and run the offline mock counter. Never put a token in
a clone URL, YAML or documentation. `Repository not found` can mean the active
account lacks access or has not accepted its invitation.

Start with the matching row above: README files for presentation, run YAML for
task/seed/budgets, agent YAML for components and endpoints, and `cli.py` for command
handling. Owners with write access can use GitHub's **Edit this file** and
**Commit changes** controls. Follow [development](development.md) before changing
runtime behavior; model credentials remain external environment variables.

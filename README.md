# Rcode

本地运行的 AI Agent 系统，参考 Claude Code 核心架构实现。

## 核心理念

```
Agent = Model (LLM) + Harness (运行环境)
```

Rcode 实现的就是这个 **Harness**：用户输入 → Agent Loop → 工具调用 → 结果回填 → 事件展示 → 会话续航。

## 功能特性

- Agent Loop：ReAct 循环
- Tool System：可扩展的工具系统
- Permission System：权限审批
- Event System：事件总线
- Session Management：会话管理
- Context Compaction：上下文压缩
- Memory System：持久化记忆
- Task System：任务管理
- Skill System：技能加载
- Subagent System：子 Agent
- MCP Integration：外部工具接入

## 快速开始

```bash
# 安装依赖
uv sync

# 启动守护进程
rcode-core

# 发送 ping 命令
rcode ping
```

## 开发

```bash
# 安装开发依赖
uv sync --extra dev

# 运行测试
uv run pytest tests/ -v

# 代码检查
uv run ruff check src/
uv run mypy src/
```

## 文档

详见 [docs/](docs/) 目录。

## 版本

- 当前版本：v0.1.0（开发中）
- 设计文档：[/home/deng/workspace/note/Rcode](/home/deng/workspace/note/Rcode)

## 许可证

MIT
# v0.2 Agent 最小闭环 — 文档更新计划

> Spec: `20260712-v02-agent-loop`
> 阶段：文档更新
> 日期：2026-07-12

## 1. 更新清单

| 文档 | 更新内容 | 状态 |
|------|----------|------|
| docs/changelog/v0.2.md | 版本变更记录 | ✅ |
| CLAUDE.md | 添加 rcode run 命令说明 | ⏳ |

## 2. CLAUDE.md 更新

### 2.1 新增内容

```markdown
## 开发命令

```bash
uv run rcode-core          # 启动 Core
uv run rcode ping          # 测试连接
uv run rcode run --goal "xxx"  # 执行 Agent 任务
uv run python -m pytest tests/ -v  # 运行测试
```
```

## 3. CHANGELOG 更新

已创建 `docs/changelog/v0.2.md`

## 4. 其他文档

| 文档 | 更新内容 | 状态 |
|------|----------|------|
| docs/api/tools.md | 添加 BaseTool、ToolResult 接口 | ⏳ |
| docs/api/llm.md | 添加 LLMProvider 接口 | ⏳ |
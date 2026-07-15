# Session ↔ Runner 接线重构 — 文档更新计划

> Spec: `20260715-v0.7.1-session-runner`
> 阶段：文档更新
> 日期：2026-07-16

## 1. 更新清单

| 文档 | 更新内容 | 状态 |
|------|----------|------|
| CLAUDE.md | 无需更新（已精简） | [x] |
| CHANGELOG | 版本变更记录 | [x] |
| 架构文档 | 无需更新 | [x] |

## 2. CHANGELOG 更新

```markdown
## [v0.7.1] - 2026-07-16

### 变更（Changed）
- AgentRunner.run() 签名变更：支持 run(session_id, user_input) 模式
- SessionManager 新增 load()、load_context()、save() 方法
- 新增 SessionAttachedEvent、SessionDetachedEvent 事件类型

### 向后兼容
- 旧的 run(goal) 模式仍可用
```

## 3. 其他文档

| 文档 | 更新内容 | 状态 |
|------|----------|------|
| — | — | [x] |

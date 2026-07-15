# Session ↔ Runner 接线重构 — 需求文档

> Spec: `20260715-v0.7.1-session-runner`
> 阶段：需求阐述
> 日期：2026-07-15
> 状态：待确认

## 1. 背景与目标

### 1.1 背景

当前 `AgentRunner.run(goal)` 每次都是一次性任务，没有 session 概念。`SessionManager` 虽已实现（v0.6），但从未被 `AgentRunner` 调用——"零件造好了，没装到车上"。

| 问题 | 代码证据 | 影响 |
|------|----------|------|
| run 每次新建 ExecutionContext | `AgentRunner.run(goal)` 直接 `ExecutionContext(goal=goal)` | 无法多轮 |
| SessionManager 未被调用 | 全文无 `SessionManager` 引用 | resume 不可用 |
| 无 session 跟踪 | run 结束后消息丢失 | 会话不持久 |

### 1.2 目标

将 SessionManager 接入 AgentRunner 主循环，实现多轮对话和 resume 能力。

- 同一 session_id 连续两次 run，第二次能看到第一次的对话历史
- 保持向后兼容，旧的 `run(goal)` 模式仍可用

---

## 2. 用户场景

### 2.1 目标用户

开发者，使用 Rcode 进行代码开发和调试。

### 2.2 使用场景

| 场景 | 用户 | 触发条件 | 期望结果 |
|------|------|----------|----------|
| 多轮对话 | 开发者 | 同一 session_id 连续两次 run | 第二次能看到第一次的历史 |
| 一次性任务 | 开发者 | 只传 goal，不传 session_id | 行为与之前一致（向后兼容） |

---

## 3. 功能范围

### 3.1 做什么（In Scope）

- [ ] run 签名变更：支持 `run(session_id, user_input)` 模式
- [ ] SessionManager 接线：run 时加载/创建 session，结束时写回
- [ ] 新增事件：`session.attached` / `session.detached`
- [ ] 向后兼容：旧的 `run(goal)` 模式仍可用

### 3.2 不做什么（Out of Scope）

- 不做状态机扩展（留 v0.12）
- 不做 `--resume` CLI 参数（留 v0.12.2）
- 不做跨进程并发写保护（留 v0.12.3）

---

## 4. 验收标准

| 编号 | 验收条件 | 优先级 |
|------|----------|--------|
| AC-01 | 同一 session_id 连续两次 run，第二次能读到第一次的 messages | P0 |
| AC-02 | 无 session_id 时保持原有一次性行为（向后兼容） | P0 |
| AC-03 | `session.load` 失败时明确报错，不静默新建 | P1 |
| AC-04 | `session.attached / session.detached` 事件正确发出 | P1 |
| AC-05 | 所有现有测试仍通过 | P0 |

---

## 5. 非功能需求

### 5.1 性能

- 无特殊性能要求

### 5.2 安全

- 无特殊安全要求

### 5.3 兼容性

- 向后兼容：旧的 `run(goal)` 模式仍可用

---

## 6. 依赖关系

| 依赖项 | 类型 | 说明 |
|--------|------|------|
| v0.6 SessionManager | 内部模块 | 已实现，需要接入 |

---

## 7. 开放问题

| 编号 | 问题 | 状态 | 结论 |
|------|------|------|------|
| Q1 | 旧签名 `run(goal)` 如何保持向后兼容？ | 待确认 | 无 user_input 时创建一次性 session |

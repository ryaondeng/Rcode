# Compactor ↔ Loop 接线重构 — 需求文档

> Spec: `20260716-v072-compactor-loop`
> 阶段：需求阐述
> 日期：2026-07-16
> 状态：待确认

## 1. 背景与目标

### 1.1 背景

目前 `Compactor` 和 `truncate_tool_results` 已实现（v0.7），但 `AgentLoop.run` 里从未调用它们——上下文永远不会真的压缩，token 超限会直接中断。

| 问题 | 代码证据 | 影响 |
|------|----------|------|
| budget.check 未调用 | `AgentLoop.run` 无水位检查 | token 超限会中断 |
| compactor 未调用 | 无 `compact_messages` 调用 | 历史消息无限增长 |
| 无 replace_history | ExecutionContext 无此方法 | runtime 无法替换旧消息 |

### 1.2 目标

将 Compactor 接入 AgentLoop 主循环，实现上下文自动压缩。

- 每步开始前检查水位
- 超水位时触发压缩
- 压缩失败时不中断主循环

---

## 2. 用户场景

### 2.1 目标用户

开发者，使用 Rcode 进行长对话任务。

### 2.2 使用场景

| 场景 | 用户 | 触发条件 | 期望结果 |
|------|------|----------|----------|
| 长对话 | 开发者 | 消息数量超水位 | 自动压缩历史 |
| 压缩失败 | 开发者 | LLM 调用失败 | 保持原 messages，不中断 |

---

## 3. 功能范围

### 3.1 做什么（In Scope）

- [ ] TokenBudget 水位检查
- [ ] AgentLoop 接入 Compactor
- [ ] ExecutionContext.replace_history 方法
- [ ] compact 触发/完成/失败事件
- [ ] Runner 传入 Compactor

### 3.2 不做什么（Out of Scope）

- 不做智能焦点选择（留 v0.14）
- 不做多档水位（暂只支持单档 70%）
- 不做手动 compact 命令（留 v0.12.1）

---

## 4. 验收标准

| 编号 | 验收条件 | 优先级 |
|------|----------|--------|
| AC-01 | 构造超预算消息，能观察到 triggered → finished 事件闭环 | P0 |
| AC-02 | 压缩失败时保持原 messages，主循环继续 | P0 |
| AC-03 | compact 事件带 before_tokens / after_tokens / ratio | P1 |
| AC-04 | auto_threshold = 0.0 时完全不触发压缩 | P0 |
| AC-05 | 所有现有测试仍通过 | P0 |

---

## 5. 非功能需求

### 5.1 性能

- 无特殊性能要求

### 5.2 安全

- 无特殊安全要求

### 5.3 兼容性

- 向后兼容：auto_threshold = 0.0 时行为不变

---

## 6. 依赖关系

| 依赖项 | 类型 | 说明 |
|--------|------|------|
| v0.7 Compactor | 内部模块 | 已实现，需要接入 |

---

## 7. 开放问题

| 编号 | 问题 | 状态 | 结论 |
|------|------|------|------|
| Q1 | TokenBudget 默认阈值是多少？ | 待确认 | 70% |

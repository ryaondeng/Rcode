# Compactor ↔ Loop 接线重构 — 完成记录

> Spec: `20260716-v072-compactor-loop`
> 阶段：完成记录
> 日期：2026-07-16

## 任务清单

- [x] T01 — 新增 CompactTriggeredEvent 事件类型
- [x] T02 — 新增 CompactFinishedEvent 事件类型
- [x] T03 — 新增 CompactFailedEvent 事件类型
- [x] T04 — TokenBudget 添加 check() 方法
- [x] T05 — ExecutionContext 添加 replace_history() 方法
- [x] T06 — AgentLoop 接入 TokenBudget 和 Compactor
- [x] T07 — AgentLoop 添加 _do_compact() 方法
- [x] T08 — Runner 传入 Compactor 和 compact_threshold
- [x] T09 — 单元测试：TokenBudget.check()
- [x] T10 — 单元测试：ExecutionContext.replace_history()
- [x] T11 — 单元测试：AgentLoop 压缩流程
- [x] T12 — 集成测试：超预算触发压缩

## Commit 记录

| 序号 | Commit | 任务 | 说明 | 时间 |
|------|--------|------|------|------|
| 1 | — | T01-T12 | refactor(v0.7.2): 实现 Compactor ↔ Loop 接线重构 | 2026-07-16 |

## 实现概览

| 指标 | 数值 |
|------|------|
| 已完成任务 | 12/12 |
| 提交数 | 1 |
| 新增文件 | 3 |
| 修改文件 | 5 |

## 已知限制

- 默认 compact_threshold=0.0，禁用自动压缩
- 需要用户显式设置阈值才能启用压缩

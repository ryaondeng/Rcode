# 事件订阅装配解耦 — 完成记录

> Spec: `20260716-v073-event-subscriber-decouple`
> 阶段：完成记录
> 日期：2026-07-16

## 任务清单

- [x] T01 — 新增 SubscriberRegistry 类
- [x] T02 — 新增 build_default_subscribers 工厂函数
- [x] T03 — 新增 cli/printer.py
- [x] T04 — 从 runner.py 移除 _EventPrinter
- [x] T05 — Runner 使用 registry 订阅事件
- [x] T06 — 单元测试：SubscriberRegistry
- [x] T07 — 单元测试：ConsoleSubscriber
- [x] T08 — 集成测试：错误隔离

## Commit 记录

| 序号 | Commit | 任务 | 说明 | 时间 |
|------|--------|------|------|------|
| 1 | — | T01-T08 | refactor(v0.7.3): 实现事件订阅装配解耦 | 2026-07-16 |

## 实现概览

| 指标 | 数值 |
|------|------|
| 已完成任务 | 8/8 |
| 提交数 | 1 |
| 新增文件 | 3 |
| 修改文件 | 2 |

## 已知限制

- 默认订阅者只有 ConsoleSubscriber
- TraceEventSubscriber 仍在 runner.py 中硬编码

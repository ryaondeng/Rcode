# v0.4 事件流 — 设计文档

> Spec: `20260713-v04-event-system`
> 阶段：设计规划
> 日期：2026-07-13
> 状态：待确认

## 1. 设计目标

实现事件系统，将 Agent 执行过程通过 EventBus 实时外化。

**核心原则**：
- 发布-订阅模式解耦事件生产者和消费者
- 异步发布，不阻塞主流程
- JSONL 格式持久化事件

## 2. 事件系统架构

```
EventBus (发布-订阅总线)
    ↓ subscribe
EventWriter (事件持久化) → events.jsonl
    ↑ publish
Event 类型 (Pydantic 模型)
```

## 3. 事件类型

| 分类 | 事件 | type 字段 |
|------|------|-----------|
| Run 生命周期 | RunStartedEvent | `run.started` |
| Run 生命周期 | RunFinishedEvent | `run.finished` |
| Step 生命周期 | StepStartedEvent | `step.started` |
| Step 生命周期 | StepFinishedEvent | `step.finished` |
| 工具调用 | ToolCallStartedEvent | `tool.call_started` |
| 工具调用 | ToolCallFinishedEvent | `tool.call_finished` |
| LLM 监控 | LlmCallStartedEvent | `llm.call_started` |
| LLM 监控 | LlmCallFinishedEvent | `llm.call_finished` |

## 4. 事件文件格式

```
.events/
└── run_{timestamp}_{random}.jsonl
```

每行一个 JSON 对象，支持流式读取。

## 5. 目录结构

```
src/rcode/core/events/
├── __init__.py
├── bus.py           # EventBus
├── types.py         # 事件类型定义
└── writer.py        # EventWriter
```
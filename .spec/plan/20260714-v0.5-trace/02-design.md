# v0.5 Trace 追踪 — 设计文档

> Spec: `20260714-v05-trace`
> 阶段：设计规划
> 日期：2026-07-14
> 状态：待确认

## 1. 设计目标

实现 Trace 系统，记录完整的执行时间线，支持回放分析。

**核心原则**：
- 统一数据模型覆盖三层
- 非阻塞写入不阻塞主流程
- 装饰器模式追踪 LLM

## 2. Trace 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    TraceWriter                          │
│   asyncio.Queue → _drain() → JSONL file (append)       │
└──────────────────────┬──────────────────────────────────┘
                       │ emit(TraceRecord)
          ┌────────────┼────────────────┐
          ▼            ▼                ▼
   ┌──────────┐  ┌──────────┐   ┌──────────────┐
   │ IPC 层   │  │ Event 层 │   │   LLM 层     │
   │          │  │          │   │              │
   │ SocketServer     EventBus订阅     TracingProvider
   └──────────┘  └──────────┘   └──────────────┘
```

## 3. 数据模型

### TraceRecord

```python
class TraceRecord(BaseModel):
    ts: str                                    # ISO-8601 UTC 时间戳
    direction: Literal[                        # 消息流向
        "CLIENT→CORE", "CORE→CLIENT",         # IPC 层
        "CORE",                               # Event 层
        "CORE→LLM", "LLM→CORE",              # LLM 层
    ]
    layer: Literal["ipc", "event", "llm"]     # 三层分类
    kind: str                                  # 语义类型
    run_id: str | None = None                  # 关联的 agent run
    step: int | None = None                    # run 中的步骤序号
    client_id: str | None = None              # IPC 客户端标识
    data: dict[str, Any]                       # 载荷数据
```

## 4. 模块设计

| 模块 | 职责 |
|------|------|
| `trace/record.py` | TraceRecord 数据结构 |
| `trace/writer.py` | TraceWriter 异步写入 |
| `trace/provider.py` | TracingProvider 装饰器 |

## 5. 目录结构

```
src/rcode/core/trace/
├── __init__.py
├── record.py       # TraceRecord
├── writer.py       # TraceWriter
└── provider.py     # TracingProvider
```
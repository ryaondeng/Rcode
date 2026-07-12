# 事件系统设计

## 核心概念

事件系统采用**发布-订阅模式**，实现系统各模块之间的解耦。

## EventBus

```python
class EventBus:
    def __init__(self):
        self._subscribers: list[EventHandler] = []
    
    def subscribe(self, handler: EventHandler):
        self._subscribers.append(handler)
    
    async def publish(self, event: BaseModel):
        for handler in self._subscribers:
            await handler(event)
```

## 设计原则

1. **解耦**：发布者不知道订阅者，订阅者不知道发布者
2. **异步**：所有 handler 都是 async，不阻塞主流程
3. **顺序保证**：按注册顺序依次调用，保证事件顺序

## 事件类型

### 运行事件
- `RunStartedEvent`：任务开始
- `RunFinishedEvent`：任务完成

### 步骤事件
- `StepStartedEvent`：步骤开始
- `StepFinishedEvent`：步骤完成

### 工具事件
- `ToolCalledEvent`：工具调用
- `ToolResultEvent`：工具结果

### 权限事件
- `ApprovalRequestEvent`：审批请求
- `ApprovalResponseEvent`：审批响应

## 事件持久化

事件通过 `EventWriter` 持久化到 JSONL 文件：

```
.events/
├── run_123.jsonl
├── run_456.jsonl
└── ...
```

每个文件包含一次运行的所有事件，按时间顺序排列。

## 使用场景

1. **实时监控**：订阅事件流，实时显示 Agent 执行状态
2. **调试分析**：回放事件流，分析 Agent 行为
3. **审计追踪**：记录所有操作，满足合规要求

## 相关文件

- `src/rcode/core/events/bus.py`：EventBus 实现
- `src/rcode/core/events/writer.py`：事件持久化
- `src/rcode/core/bus/events.py`：事件类型定义
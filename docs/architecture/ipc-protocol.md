# IPC 协议设计

## 协议选择

**JSON-RPC 2.0 over NDJSON**

- **JSON-RPC 2.0**：成熟标准，有明确的请求/响应/错误格式
- **NDJSON**：每行一个 JSON 对象，便于流式读取，不需要处理消息边界
- **类型安全**：配合 Pydantic 模型，在协议层保证数据正确性

## 消息格式

### 请求 (Request)

```json
{
  "jsonrpc": "2.0",
  "method": "ping",
  "params": {},
  "id": "req_123"
}
```

### 成功响应 (Success)

```json
{
  "jsonrpc": "2.0",
  "result": {"type": "pong", "ts": "2026-07-12T10:00:00Z"},
  "id": "req_123"
}
```

### 错误响应 (Error)

```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32600, "message": "Invalid Request"},
  "id": "req_123"
}
```

## 命令定义

| 命令 | 说明 | 参数 |
|------|------|------|
| `ping` | 心跳检测 | - |
| `run` | 执行任务 | `goal: str` |
| `chat` | 多轮对话 | `message: str, session_id?: str` |
| `subscribe` | 订阅事件 | `topics?: list[str]` |

## 事件定义

| 事件 | 说明 |
|------|------|
| `run_started` | 任务开始 |
| `step_started` | 步骤开始 |
| `tool_called` | 工具调用 |
| `tool_result` | 工具结果 |
| `run_finished` | 任务完成 |

## 类型定义

详见 `src/rcode/core/bus/` 目录：
- `envelope.py`：JSON-RPC 信封模型
- `commands.py`：命令联合类型
- `events.py`：事件联合类型
# v0.4 事件流 — 单元测试报告

> Spec: `20260713-v04-event-system`
> 阶段：单元测试
> 日期：2026-07-13

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 11 |
| 通过 | 11 |
| 失败 | 0 |
| 整体覆盖率 | 95% |

## 2. 测试用例清单

### 2.1 EventBus（3 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_event_bus_subscribe_and_publish | 订阅和发布 | 收到事件 | [x] |
| test_event_bus_multiple_subscribers | 多个订阅者 | 所有订阅者收到 | [x] |
| test_event_bus_order | 订阅顺序 | 按顺序调用 | [x] |

### 2.2 事件类型（8 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_run_started_event | Run 开始 | 序列化正确 | [x] |
| test_run_finished_event | Run 结束 | 序列化正确 | [x] |
| test_step_started_event | Step 开始 | 序列化正确 | [x] |
| test_step_finished_event | Step 结束 | 序列化正确 | [x] |
| test_tool_call_started_event | 工具调用开始 | 序列化正确 | [x] |
| test_tool_call_finished_event | 工具调用结束 | 序列化正确 | [x] |
| test_llm_call_started_event | LLM 调用开始 | 序列化正确 | [x] |
| test_llm_call_finished_event | LLM 调用结束 | 序列化正确 | [x] |

## 3. 测试执行命令

```bash
uv run python -m pytest tests/unit/test_events/ -v
```
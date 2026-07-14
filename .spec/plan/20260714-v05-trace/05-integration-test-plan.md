# v0.5 Trace 追踪 — 集成测试报告

> Spec: `20260714-v05-trace`
> 阶段：集成测试
> 日期：2026-07-14

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 2 |
| 通过 | 2 |
| 失败 | 0 |

## 2. 测试场景

### 2.1 完整 Trace 流程

| 场景 | 涉及模块 | 测试步骤 | 期望结果 | 状态 |
|------|----------|----------|----------|------|
| LLM 调用追踪 | TracingProvider + TraceWriter | 调用 LLM | 记录 api_call/api_response | [x] |

### 2.2 EventBus 集成

| 场景 | 涉及模块 | 测试步骤 | 期望结果 | 状态 |
|------|----------|----------|----------|------|
| 事件追踪 | EventBus + TraceWriter | 发布事件 | 事件被记录 | [x] |

## 3. 测试执行命令

```bash
uv run python -m pytest tests/integration/test_trace.py -v
```
# Session ↔ Runner 接线重构 — 单元测试报告

> Spec: `20260715-v0.7.1-session-runner`
> 阶段：单元测试
> 日期：2026-07-16

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 130 |
| 通过 | 130 |
| 失败 | 0 |
| 跳过 | 0 |
| 总覆盖率 | 77% |
| runner.py 覆盖率 | 85% |

## 2. 测试用例清单

### 2.1 核心业务逻辑

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_session_create | 创建新 session | session 正确创建 | [x] |
| test_session_load | 加载已有 session | session 正确加载 | [x] |
| test_session_load_not_found | session 不存在 | 返回 None | [x] |

### 2.2 边界条件

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_session_save | 保存消息到 session | 消息正确保存 | [x] |
| test_session_get_history | 获取会话历史 | 历史正确返回 | [x] |

### 2.3 v0.7.1 新增测试

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_load_session | 加载 session | session 正确加载 | [x] |
| test_load_session_not_found | session 不存在 | 返回 None | [x] |
| test_load_context | 加载执行上下文 | context 正确构建 | [x] |
| test_load_context_not_found | session 不存在 | 返回 None | [x] |
| test_save_messages | 保存消息列表 | 消息正确保存 | [x] |
| test_create_session_with_id | 指定 session_id | session 正确创建 | [x] |
| test_agent_runner_init | Runner 初始化 | 组件正确初始化 | [x] |
| test_agent_runner_register_builtin_tools | 注册内置工具 | 6 个工具已注册 | [x] |
| test_agent_runner_run_old_mode | 旧模式 run | 创建一次性 session | [x] |
| test_agent_runner_run_new_mode | 新模式 run | 加载指定 session | [x] |
| test_run_outcome | RunOutcome 数据类 | 字段正确赋值 | [x] |
| test_run_outcome_failed | RunOutcome 失败 | status="failed" | [x] |
| test_run_outcome_empty_result | RunOutcome 空结果 | result="" | [x] |
| test_event_printer_run_started | 打印启动事件 | 输出 Task | [x] |
| test_event_printer_run_finished | 打印结束事件 | 输出 Done | [x] |
| test_event_printer_tool_call_started | 打印工具调用 | 输出工具名 | [x] |
| test_event_printer_tool_call_finished | 打印工具完成 | 输出结果 | [x] |
| test_event_printer_llm_call_started | 打印 LLM 调用 | 输出 LLM | [x] |
| test_event_printer_long_tool_result | 长结果截断 | 输出 ... | [x] |
| test_event_printer_empty_tool_result | 空结果不打印 | 无 Output | [x] |

## 3. 测试执行命令

```bash
# 运行所有单元测试
uv run python -m pytest tests/unit/ -v
```

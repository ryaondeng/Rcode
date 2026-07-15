# v0.6 会话管理 — 单元测试报告

> Spec: `20260714-v06-session`
> 阶段：单元测试
> 日期：2026-07-14

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 12 |
| 通过 | 12 |
| 失败 | 0 |
| 整体覆盖率 | 90% |

## 2. 测试用例清单

### 2.1 Session Model（2 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_session_serialization | 序列化 | 字段正确 | [x] |
| test_session_from_dict | 反序列化 | 对象正确 | [x] |

### 2.2 SessionStore（4 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_write_and_read_meta | 写入读取元数据 | 数据一致 | [x] |
| test_read_meta_not_found | 读取不存在 | 返回 None | [x] |
| test_append_and_read_messages | 追加读取消息 | 消息正确 | [x] |
| test_append_and_read_notes | 追加读取笔记 | 笔记正确 | [x] |

### 2.3 SessionManager（6 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_create_session | 创建会话 | 会话创建成功 | [x] |
| test_send_message | 发送消息 | 返回 run_id | [x] |
| test_send_message_not_found | 会话不存在 | 抛出异常 | [x] |
| test_send_message_closed | 会话已关闭 | 抛出异常 | [x] |
| test_get_history | 获取历史 | 历史正确 | [x] |
| test_close_session | 关闭会话 | 状态变为 closed | [x] |

## 3. 测试执行命令

```bash
uv run python -m pytest tests/unit/test_session/ -v
```
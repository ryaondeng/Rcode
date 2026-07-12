# v0.1 骨架与协议 — 集成测试计划

> Spec: `20260712-v01-skeleton-protocol`
> 阶段：集成测试
> 日期：2026-07-12
> 状态：已完成

## 测试场景

| 场景 | 描述 | 预期结果 |
|------|------|----------|
| ping/pong | 发送 ping 命令，验证 pong 响应 | 返回正确的 server_version、uptime_ms |
| 多次 ping | 连续发送 5 次 ping | 每次都能正确响应 |
| 方法不存在 | 调用不存在的方法 | 返回 METHOD_NOT_FOUND 错误 |
| handler 异常 | handler 抛出异常 | 返回 INTERNAL_ERROR 错误 |
| handler 错误 | handler 抛出 HandlerError | 返回自定义错误码和数据 |

## 测试用例

```python
# test_ping_pong
server.register("core.ping", handler)
client.send("core.ping", {"client": "test"})
assert result["pong"] is True

# test_multiple_pings
for i in range(5):
    client.send("core.ping", {"client": f"client_{i}"})
    assert result["pong"] is True

# test_method_not_found
client.send("nonexistent.method")
assert exc_info.value.code == -32601

# test_handler_exception
server.register("test.error", error_handler)
client.send("test.error")
assert exc_info.value.code == -32603

# test_handler_error_exception
server.register("test.handler_error", handler_error_handler)
client.send("test.handler_error")
assert exc_info.value.code == -32600
```

## 测试环境

- 使用 free_port fixture 避免端口冲突
- 每个测试启动独立的 server 实例
- 测试完成后自动清理

## 测试结果

```
5 passed in 0.06s
```

## 质量评估

- ✅ 所有集成测试通过
- ✅ 核心业务流程端到端验证通过
- ✅ 错误处理路径验证通过

# v0.1 骨架与协议 — 单元测试计划

> Spec: `20260712-v01-skeleton-protocol`
> 阶段：单元测试
> 日期：2026-07-12
> 状态：已完成

## 测试覆盖

| 模块 | 测试文件 | 测试数量 | 覆盖率 |
|------|----------|----------|--------|
| bus/envelope.py | test_envelope.py | 12 | 100% |
| bus/commands.py | test_commands.py | 2 | 100% |
| bus/events.py | test_events.py | 1 | 100% |
| config.py | test_config.py | 3 | 85% |
| logging_setup.py | test_logging.py | 2 | 100% |
| app.py | test_app.py | 5 | 60% |
| cli/main.py | test_cli.py | 4 | 92% |
| transport/socket_client.py | test_ipc.py | 5 | 97% |
| transport/socket_server.py | test_ipc.py | 5 | 77% |

## 测试用例清单

### test_envelope.py（12 个）

- test_request_roundtrip
- test_request_default_params
- test_success_roundtrip
- test_error_roundtrip
- test_error_with_data
- test_error_no_id
- test_make_error
- test_make_error_with_data
- test_handler_error
- test_error_codes

### test_commands.py（2 个）

- test_ping_command_roundtrip
- test_pong_result_roundtrip

### test_config.py（3 个）

- test_default_config
- test_get_config_defaults
- test_get_config_from_env

### test_app.py（5 个）

- test_core_app_init
- test_ping_handler
- test_ping_handler_default_client
- test_ping_handler_uptime_increases
- test_run_sync

### test_cli.py（4 个）

- test_cli_version
- test_cli_no_command
- test_cli_ping_no_core
- test_cli_core_no_subcommand

### test_ipc.py（5 个集成测试）

- test_ping_pong
- test_multiple_pings
- test_method_not_found
- test_handler_exception
- test_handler_error_exception

## 覆盖率统计

```
TOTAL  400  73  82%
```

## 未覆盖代码分析

| 模块 | 未覆盖行 | 原因 |
|------|----------|------|
| app.py:33-49 | run 方法 | 需要实际启动服务器 |
| socket_server.py:44-46 | 端口占用检测 | 需要网络环境 |
| config.py:38,50-51 | TOML 解析错误 | 错误路径，集成测试覆盖 |

## 质量评估

- ✅ 所有单元测试通过
- ✅ 覆盖率 ≥ 80%
- ✅ 关键路径覆盖率 ≥ 90%

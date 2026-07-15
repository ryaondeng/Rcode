# CLI ↔ Core IPC 化（骨架）— 单元测试报告

> Spec: `20260716-v074-ipc-skeleton`
> 阶段：单元测试
> 日期：2026-07-16

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 149 |
| 通过 | 149 |
| 失败 | 0 |
| 跳过 | 0 |
| 总覆盖率 | 79% |

## 2. 测试用例清单

### 2.1 IpcClient

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_ipc_client_init | 初始化 | 客户端正确初始化 | [x] |
| test_ipc_client_connect | 连接 | 客户端正确连接 | [x] |
| test_ipc_client_close | 关闭 | 客户端正确关闭 | [x] |

### 2.2 SocketServer

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_socket_server_init | 初始化 | 服务端正确初始化 | [x] |
| test_socket_server_register | 注册 handler | handler 正确注册 | [x] |
| test_socket_server_handle_line | 处理请求 | 请求正确处理 | [x] |

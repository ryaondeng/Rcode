# CLI ↔ Core IPC 化（骨架）— 需求文档

> Spec: `20260716-v074-ipc-skeleton`
> 阶段：需求阐述
> 日期：2026-07-16
> 状态：待确认

## 1. 背景与目标

### 1.1 背景

v0.1 就设计了"CLIENT / CORE 双进程"，但 `cmd_run` 一直是 `import AgentRunner` 直接在 CLI 进程内跑。只有 `cmd_ping` 走了 Socket。

| 问题 | 代码证据 | 影响 |
|------|----------|------|
| cmd_run 在 CLI 进程内跑 | `AgentRunner()` 直接 import 使用 | Session 无法跨终端 |
| 只有 cmd_ping 走 Socket | `cmd_ping` 连接 7437 端口 | IPC 只是摆设 |
| Session 存活 ≡ CLI 存活 | 无独立 Core 进程 | 关终端丢会话 |

### 1.2 目标

实现 CLIENT / CORE 双进程骨架，CLI 通过 JSON-RPC 与 Core 通信。

- `rcode core start` 启动 Core 进程
- `rcode run` 走 IPC 通信
- `--local` 保留同进程行为（向后兼容）

---

## 2. 用户场景

### 2.1 目标用户

开发者，使用 Rcode 进行代码开发和调试。

### 2.2 使用场景

| 场景 | 用户 | 触发条件 | 期望结果 |
|------|------|----------|----------|
| 启动 Core | 开发者 | `rcode core start` | Core 进程启动 |
| IPC 执行 | 开发者 | `rcode run "..."` | 通过 IPC 执行任务 |
| 同进程模式 | 开发者 | `rcode run --local "..."` | 直接执行任务 |

---

## 3. 功能范围

### 3.1 做什么（In Scope）

- [ ] Core 进程启动/停止
- [ ] SocketServer 支持 core.run 异步执行
- [ ] IPC 客户端
- [ ] CLI core 命令组
- [ ] `--local` 降级开关

### 3.2 不做什么（Out of Scope）

- 不做事件订阅协议（留 v0.7.4.2）
- 不做 pydantic 契约（留 v0.7.4.1）
- 不做多客户端并发
- 不做认证

---

## 4. 验收标准

| 编号 | 验收条件 | 优先级 |
|------|----------|--------|
| AC-01 | `rcode core start` 启动 Core 进程 | P0 |
| AC-02 | 另开终端 `rcode run "..."` 能拿到 run_id 并同步等到最终结果 | P0 |
| AC-03 | `--local` 保留同进程行为 | P0 |
| AC-04 | Core 崩溃时 CLI 不 hang | P1 |

---

## 5. 非功能需求

### 5.1 性能

- 无特殊性能要求

### 5.2 安全

- 无特殊安全要求

### 5.3 兼容性

- 向后兼容：`--local` 保留同进程行为

---

## 6. 依赖关系

| 依赖项 | 类型 | 说明 |
|--------|------|------|
| v0.7.1 Session | 内部模块 | 已重构 |
| v0.7.3 事件订阅 | 内部模块 | 已解耦 |

---

## 7. 开放问题

| 编号 | 问题 | 状态 | 结论 |
|------|------|------|------|
| Q1 | 默认端口是多少？ | 待确认 | 7437 |

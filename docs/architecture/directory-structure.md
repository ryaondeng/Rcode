# 目录结构

## 项目根目录

```
rcode/
├── src/                     # 源代码
├── tests/                   # 测试
├── docs/                    # 文档
├── skills/                  # 技能包
├── pyproject.toml           # 项目配置
├── CLAUDE.md                # 开发指南
└── README.md                # 项目说明
```

## 源代码目录

```
src/
└── rcode/                   # 顶层包
    ├── __init__.py
    ├── core/                # 核心模块
    │   ├── __init__.py
    │   ├── app.py           # 守护进程入口
    │   ├── loop.py          # Agent Loop 核心
    │   ├── runner.py        # 运行器，组装依赖
    │   ├── context.py       # 执行上下文
    │   ├── config.py        # 配置管理
    │   │
    │   ├── bus/             # IPC 协议层
    │   │   ├── envelope.py  # JSON-RPC 信封
    │   │   ├── commands.py  # 命令定义
    │   │   └── events.py    # 事件定义
    │   │
    │   ├── transport/       # 传输层
    │   │   ├── socket_server.py # TCP 服务端
    │   │   └── socket_client.py # TCP 客户端
    │   │
    │   ├── llm/             # LLM 接口
    │   │   ├── base.py      # 抽象基类
    │   │   ├── provider.py  # Anthropic 实现
    │   │   └── types.py     # 类型定义
    │   │
    │   ├── tools/           # 工具系统
    │   │   ├── base.py      # 工具基类
    │   │   ├── registry.py  # 工具注册表
    │   │   ├── invocation.py # 工具调用逻辑
    │   │   ├── errors.py    # 工具错误类型
    │   │   └── builtin/     # 内置工具
    │   │
    │   ├── permissions/     # 权限系统
    │   ├── events/          # 事件系统
    │   ├── session/         # 会话管理
    │   ├── memory/          # 记忆系统
    │   ├── compact/         # 上下文压缩
    │   ├── task/            # 任务系统
    │   ├── subagent/        # 子 Agent
    │   ├── skills/          # 技能系统
    │   ├── mcp/             # MCP 集成
    │   ├── trace/           # 追踪系统
    │   │
    │   ├── hooks/           # Hook 系统 (v0.15)
    │   ├── prompt/          # Prompt 组装 (v0.17)
    │   ├── background/      # 后台任务 (v0.18)
    │   ├── scheduler/       # 定时任务 (v0.19)
    │   ├── teams/           # Agent 团队 (v0.20)
    │   └── worktree/        # 工作树隔离 (v0.21)
    │
    ├── cli/                 # CLI 客户端
    │   ├── __init__.py
    │   ├── main.py
    │   └── commands/
    │
    └── tui/                 # TUI 客户端（可选）
        ├── __init__.py
        └── app.py
```

## 测试目录

```
tests/
├── __init__.py
├── conftest.py              # pytest fixtures
├── unit/                    # 单元测试
│   ├── __init__.py
│   ├── test_loop.py
│   ├── test_tools/
│   ├── test_permissions/
│   └── ...
└── integration/             # 集成测试
    ├── __init__.py
    ├── test_ipc.py
    └── ...
```

## 文档目录

```
docs/
├── versions/                # 版本文档
├── architecture/            # 架构文档
├── development/             # 开发规范
├── api/                     # API 文档
└── changelog/               # 版本说明
```

## 模块职责

| 模块 | 职责 |
|------|------|
| `rcode/core/app.py` | 守护进程入口，启动服务 |
| `rcode/core/loop.py` | Agent Loop 核心，驱动 Think-Act-Observe 循环 |
| `rcode/core/runner.py` | 运行器，组装所有依赖 |
| `rcode/core/context.py` | 执行上下文，管理消息历史 |
| `rcode/core/config.py` | 配置管理，四级优先级加载 |
| `rcode/core/bus/` | IPC 协议定义 |
| `rcode/core/transport/` | TCP 传输层 |
| `rcode/core/llm/` | LLM 接口抽象 |
| `rcode/core/tools/` | 工具系统 |
| `rcode/core/permissions/` | 权限管理 |
| `rcode/core/events/` | 事件总线 |
| `rcode/core/session/` | 会话管理 |
| `rcode/core/memory/` | 记忆系统 |
| `rcode/core/compact/` | 上下文压缩 |
| `rcode/core/task/` | 任务系统 |
| `rcode/core/subagent/` | 子 Agent |
| `rcode/core/skills/` | 技能加载 |
| `rcode/core/mcp/` | MCP 集成 |

## 配置管理

### 四级配置优先级

```
默认值 → 全局 TOML → 项目本地 TOML → .env → 环境变量
                        (低优先级)              (高优先级)
```

| 优先级 | 配置源 | 路径 | 说明 |
|--------|--------|------|------|
| 1 | 默认值 | 代码硬编码 | 始终存在 |
| 2 | 全局 TOML | `~/.rcode/config.toml` | 用户级配置，不存在则跳过 |
| 3 | 项目 TOML | `.rcode/config.toml` | 项目级配置，不存在则跳过 |
| 4 | .env | `.env` | 环境变量文件，override=False |
| 5 | 环境变量 | `RCODE_*` | 最高优先级，覆盖所有配置 |

### 配置文件格式

TOML 格式，示例：

```toml
[core]
host = "127.0.0.1"
port = 7437

[logging]
level = "INFO"
file = "~/.rcode/logs/core.log"
```

### 设计原则

1. **零配置可用**：不创建任何配置文件也能运行
2. **渐进式配置**：用户按需创建配置文件覆盖默认值
3. **不会报错**：配置文件不存在不会导致启动失败
4. **环境变量优先**：便于容器化部署和 CI/CD
| `rcode/core/trace/` | 追踪系统 |
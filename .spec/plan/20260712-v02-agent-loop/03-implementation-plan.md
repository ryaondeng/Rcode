# v0.2 Agent 最小闭环 — 实现计划

> Spec: `20260712-v02-agent-loop`
> 阶段：设计规划
> 日期：2026-07-12
> 状态：待确认

## 任务拆解

### 阶段一：LLM 接口

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T1 | 创建 `core/llm/__init__.py` | 5min | [x] |
| T2 | 实现 `core/llm/types.py`（ChatResponse、ToolCall） | 15min | [x] |
| T3 | 实现 `core/llm/base.py`（LLMProvider ABC） | 10min | [x] |
| T4 | 实现 `core/llm/provider.py`（AnthropicProvider） | 30min | [x] |
| T5 | 配置 LLM 相关环境变量（ANTHROPIC_API_KEY、MODEL） | 5min | [x] |

### 阶段二：工具系统

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T6 | 创建 `core/tools/__init__.py` | 5min | [x] |
| T7 | 实现 `core/tools/base.py`（BaseTool、ToolResult） | 15min | [x] |
| T8 | 实现 `core/tools/registry.py`（ToolRegistry） | 15min | [x] |
| T9 | 实现 `core/tools/invocation.py`（invoke_tool） | 20min | [x] |
| T10 | 创建 `core/tools/builtin/__init__.py` | 5min | [x] |
| T11 | 实现 `core/tools/builtin/bash.py`（BashTool） | 20min | [x] |

### 阶段三：Agent Loop

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T12 | 实现 `core/context.py`（ExecutionContext） | 30min | [x] |
| T13 | 实现 `core/loop.py`（AgentLoop） | 40min | [x] |
| T14 | 实现 `core/runner.py`（AgentRunner） | 30min | [x] |

### 阶段四：CLI 集成

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T15 | 添加 `rcode run --goal` 命令 | 20min | [x] |
| T16 | 更新 `cli/main.py` 支持 run 命令 | 15min | [x] |

### 阶段五：配置更新

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T17 | 更新 `config.py` 添加 LLM 配置 | 15min | [x] |
| T18 | 更新 `.env.example` 添加 API Key 配置 | 5min | [x] |

## 任务依赖

```
阶段一：T1 → T2 → T3 → T4 → T5
                            ↓
阶段二：T6 → T7 → T8 → T9 → T10 → T11
                                    ↓
阶段三：          T12 → T13 → T14
                        ↓
阶段四：          T15 → T16
                        ↓
阶段五：          T17 → T18
```

## 优先级

- P0: T1-T5, T6-T11, T12-T14（核心功能）
- P1: T15-T16（CLI 集成）
- P2: T17-T18（配置更新）

## 预计总时间

| 阶段 | 时间 |
|------|------|
| 阶段一：LLM 接口 | 65min |
| 阶段二：工具系统 | 80min |
| 阶段三：Agent Loop | 100min |
| 阶段四：CLI 集成 | 35min |
| 阶段五：配置更新 | 20min |
| **总计** | **300min（5小时）** |

## 验证检查点

每个阶段完成后运行测试：

```bash
# 阶段一完成后
uv run python -c "from rcode.core.llm import AnthropicProvider; print('LLM OK')"

# 阶段二完成后
uv run python -c "from rcode.core.tools import BashTool; print('Tools OK')"

# 阶段三完成后
uv run python -c "from rcode.core.runner import AgentRunner; print('Runner OK')"

# 阶段四完成后
uv run rcode run --goal "echo hello"

# 所有阶段完成后
uv run python -m pytest tests/ -v
```
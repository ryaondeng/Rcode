# v0.4 事件流 — 实现计划

> Spec: `20260713-v04-event-system`
> 阶段：设计规划
> 日期：2026-07-13
> 状态：待确认

## 任务拆解

### 阶段一：事件基础设施

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T1 | 创建 `core/events/__init__.py` | 5min | [ ] |
| T2 | 实现 `core/events/bus.py`（EventBus） | 20min | [ ] |
| T3 | 实现 `core/events/types.py`（事件类型） | 30min | [ ] |
| T4 | 实现 `core/events/writer.py`（EventWriter） | 25min | [ ] |

### 阶段二：Agent Loop 集成

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T5 | 更新 `loop.py` 集成 EventBus | 30min | [ ] |
| T6 | 更新 `runner.py` 初始化 EventBus | 20min | [ ] |

### 阶段三：测试

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T7 | 编写 `test_bus.py` | 20min | [ ] |
| T8 | 编写 `test_types.py` | 20min | [ ] |
| T9 | 编写 `test_writer.py` | 20min | [ ] |
| T10 | 编写 `test_agent_events.py` | 25min | [ ] |
| T11 | 运行所有测试 | 10min | [ ] |

## 预计总时间

| 阶段 | 时间 |
|------|------|
| 阶段一：事件基础设施 | 80min |
| 阶段二：Agent Loop 集成 | 50min |
| 阶段三：测试 | 95min |
| **总计** | **225min（3.75小时）** |
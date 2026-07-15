# v0.6 会话管理 — 实现计划

> Spec: `20260714-v06-session`
> 阶段：设计规划
> 日期：2026-07-14
> 状态：待确认

## 任务拆解

### 阶段一：会话基础设施

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T1 | 创建 `core/session/__init__.py` | 5min | [ ] |
| T2 | 实现 `core/session/model.py`（Session） | 15min | [ ] |
| T3 | 实现 `core/session/store.py`（SessionStore） | 30min | [ ] |
| T4 | 实现 `core/session/manager.py`（SessionManager） | 40min | [ ] |

### 阶段二：测试

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T5 | 编写 `test_model.py` | 15min | [ ] |
| T6 | 编写 `test_store.py` | 25min | [ ] |
| T7 | 编写 `test_manager.py` | 30min | [ ] |
| T8 | 运行所有测试 | 10min | [ ] |

## 预计总时间

| 阶段 | 时间 |
|------|------|
| 阶段一：会话基础设施 | 90min |
| 阶段二：测试 | 80min |
| **总计** | **170min（2.8小时）** |
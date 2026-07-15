# v0.6 会话管理 — 设计文档

> Spec: `20260714-v06-session`
> 阶段：设计规划
> 日期：2026-07-14
> 状态：待确认

## 1. 设计目标

实现会话管理，支持多轮对话和会话持久化。

**核心原则**：
- 文件后端存储，简单可靠
- 状态机管理会话生命周期
- 每个 session 独立锁，防止并发写

## 2. 会话管理架构

```
SessionManager (业务管理)
    ↓
SessionStore (文件持久化)
    ↓
磁盘布局:
  {session_id}/
    meta.json          # Session 元信息
    thread.jsonl       # 对话历史
    notes.md           # 主动笔记
```

## 3. 数据模型

### Session

```python
@dataclass
class Session:
    id: str
    mode: Literal["one_shot", "chat"]
    status: Literal["active", "waiting_for_input", "closed"]
    title: str
    created_at: str
    updated_at: str
    run_ids: list[str]
```

## 4. 状态机

```
active → waiting_for_input → active → closed
```

## 5. 目录结构

```
src/rcode/core/session/
├── __init__.py
├── model.py       # Session 数据结构
├── store.py       # SessionStore 文件持久化
└── manager.py     # SessionManager 业务管理
```
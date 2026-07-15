# v0.7 上下文压缩 — 设计文档

> Spec: `20260714-v07-compaction`
> 阶段：设计规划
> 日期：2026-07-14
> 状态：待确认

## 1. 设计目标

实现上下文压缩，支持长对话场景下的 token 管理。

**核心原则**：
- 四层压缩管线（参考 learn-claude-code）
- 便宜的先跑，贵的后跑
- tool_use/tool_result 配对保护

## 2. 四层压缩管线

| 层 | 函数 | 成本 | 触发条件 | 操作 |
|---|---|---|---|---|
| L3 (最先) | `tool_result_budget()` | 0 API | tool_result 总量 > 200KB | 超长结果落盘 |
| L1 | `snip_compact()` | 0 API | 消息数 > 50 条 | 保留头尾，中间裁掉 |
| L2 | `micro_compact()` | 0 API | tool_result 总数 > 3 | 只保留最近 3 条 |
| L4 | `compact_history()` | 1 API | 估计 token > 50000 | LLM 生成摘要 |

## 3. 目录结构

```
src/rcode/core/compact/
├── __init__.py
├── compactor.py       # LLM 压缩器
└── budget.py          # tool_result 截断
```
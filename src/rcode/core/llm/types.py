from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ToolCall:
    """工具调用信息。"""
    id: str  # 调用 ID
    name: str  # 工具名称
    input: dict  # 输入参数


@dataclass
class ChatResponse:
    """LLM 响应。"""
    text: str | None = None  # 文本回复
    tool_calls: list[ToolCall] = field(default_factory=list)  # 工具调用列表
    stop_reason: str = "end_turn"  # 停止原因："tool_use" | "end_turn" | "max_tokens"

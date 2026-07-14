from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rcode.core.events.bus import EventBus
from rcode.core.llm.base import LLMProvider


@dataclass
class CompactionResult:
    """压缩结果。"""
    summary_text: str
    original_token_estimate: int
    summary_tokens: int


_COMPACT_PROMPT = """You are compressing a conversation history. Generate a structured summary:

## Original Goal
The user's original request.

## Completed Steps
What has been done so far.

## Key Constraints & Discoveries
Important facts learned during the conversation.

## Current File State
Current state of relevant files.

## Remaining TODOs
What still needs to be done.

## Critical Data
Any data that must be preserved for continuity."""


class Compactor:
    """LLM 驱动的上下文压缩器。"""

    def __init__(self, bus: EventBus, session_dir: Path) -> None:
        self._bus = bus
        self._session_dir = session_dir

    async def compact_messages(
        self,
        messages: list[dict],
        provider: LLMProvider,
        focus: str = "",
    ) -> CompactionResult | None:
        """纯函数式压缩，返回 CompactionResult 或 None。"""
        # 估算原始 token
        original_tokens = sum(len(str(m.get("content", ""))) // 4 for m in messages)

        # 构造压缩 prompt
        prompt = _COMPACT_PROMPT
        if focus:
            prompt += f"\n\nFocus on: {focus}"

        # 调用 LLM 生成摘要
        try:
            response = await provider.chat(
                messages=[{"role": "user", "content": f"Summarize this conversation:\n\n{self._messages_to_text(messages)}"}],
                tool_schemas=[],
                system=prompt,
            )
            summary = response.text or ""
        except Exception:
            return None

        if not summary.strip():
            return None

        summary_tokens = len(summary) // 4
        return CompactionResult(
            summary_text=summary,
            original_token_estimate=original_tokens,
            summary_tokens=summary_tokens,
        )

    def _messages_to_text(self, messages: list[dict]) -> str:
        """将消息列表转为文本。"""
        parts = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "text":
                        parts.append(f"[{role}] {block.get('text', '')}")
                    elif block.get("type") == "tool_use":
                        parts.append(f"[{role}] Tool call: {block.get('name')}")
                    elif block.get("type") == "tool_result":
                        parts.append(f"[{role}] Tool result: {str(block.get('content', ''))[:200]}")
            elif isinstance(content, str):
                parts.append(f"[{role}] {content}")
        return "\n".join(parts)

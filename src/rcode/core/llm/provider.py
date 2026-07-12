from __future__ import annotations

import logging
import os
from typing import Any

import anthropic

from rcode.core.llm.base import LLMProvider
from rcode.core.llm.types import ChatResponse, ToolCall

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    def __init__(self, model: str | None = None, client: Any = None) -> None:
        if client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise SystemExit("ANTHROPIC_API_KEY not set")
            self._client = anthropic.AsyncAnthropic(api_key=api_key)
        else:
            self._client = client
        self._model = model or os.environ.get("MODEL_ID", "claude-sonnet-4-20250514")

    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        try:
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=8096,
                system=system,
                messages=messages,
                tools=tool_schemas if tool_schemas else [],
            )
            return self._parse_response(response)
        except Exception as e:
            logger.exception("LLM call failed")
            raise

    def _parse_response(self, response: Any) -> ChatResponse:
        text = None
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text = block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(id=block.id, name=block.name, input=block.input)
                )

        return ChatResponse(
            text=text,
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
        )

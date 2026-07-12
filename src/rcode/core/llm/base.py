from __future__ import annotations

from abc import ABC, abstractmethod

from rcode.core.llm.types import ChatResponse


class LLMProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        """Send a chat request to the LLM."""
        ...

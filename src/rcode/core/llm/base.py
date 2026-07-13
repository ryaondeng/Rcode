from __future__ import annotations

from abc import ABC, abstractmethod

from rcode.core.llm.types import ChatResponse


class LLMProvider(ABC):
    """LLM 提供商抽象基类。

    所有 LLM 提供商必须实现 chat 方法。
    便于后续扩展其他提供商（如 OpenAI、DeepSeek）。
    """

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        """发送聊天请求到 LLM。

        Args:
            messages: 消息历史
            tool_schemas: 工具 schema 列表
            system: 系统提示词

        Returns:
            ChatResponse: LLM 响应
        """
        ...

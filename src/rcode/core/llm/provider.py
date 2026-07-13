from __future__ import annotations

import logging
import os
from typing import Any

import anthropic

from rcode.core.llm.base import LLMProvider
from rcode.core.llm.types import ChatResponse, ToolCall

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API 实现。

    负责：
    1. 与 Anthropic API 通信
    2. 发送消息并获取响应
    3. 解析响应为统一格式
    """

    def __init__(self, model: str | None = None, client: Any = None) -> None:
        """初始化 Anthropic Provider。

        Args:
            model: 模型名称，默认从环境变量 MODEL_ID 读取
            client: Anthropic 客户端，可选（用于测试 mock）
        """
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
        """发送聊天请求到 Anthropic API。

        Args:
            messages: 消息历史
            tool_schemas: 工具 schema 列表
            system: 系统提示词

        Returns:
            ChatResponse: 解析后的响应
        """
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
        """解析 Anthropic API 响应为 ChatResponse。"""
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

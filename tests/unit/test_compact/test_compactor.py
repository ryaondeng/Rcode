import pytest
from pathlib import Path

from rcode.core.compact.compactor import Compactor
from rcode.core.events.bus import EventBus
from rcode.core.llm.types import ChatResponse


class MockLLMProvider:
    def __init__(self, response: ChatResponse):
        self._response = response

    async def chat(self, messages, tool_schemas, system):
        return self._response


@pytest.mark.asyncio
async def test_compactor_compact_messages(tmp_path):
    bus = EventBus()
    compactor = Compactor(bus, tmp_path)

    mock_llm = MockLLMProvider(ChatResponse(text="Summary of conversation", stop_reason="end_turn"))
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]

    result = await compactor.compact_messages(messages, mock_llm)
    assert result is not None
    assert result.summary_text == "Summary of conversation"
    assert result.original_token_estimate > 0
    assert result.summary_tokens > 0


@pytest.mark.asyncio
async def test_compactor_messages_to_text(tmp_path):
    bus = EventBus()
    compactor = Compactor(bus, tmp_path)

    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]
    text = compactor._messages_to_text(messages)
    assert "[user] Hello" in text
    assert "[assistant] Hi" in text

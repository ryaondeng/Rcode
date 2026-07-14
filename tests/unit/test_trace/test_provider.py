import pytest

from rcode.core.llm.types import ChatResponse
from rcode.core.trace.provider import TracingProvider
from rcode.core.trace.writer import TraceWriter


class MockLLMProvider:
    def __init__(self, response: ChatResponse):
        self._response = response

    async def chat(self, messages, tool_schemas, system):
        return self._response


@pytest.mark.asyncio
async def test_tracing_provider_records_llm_call(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace = TraceWriter(trace_file)
    await trace.start()

    mock_llm = MockLLMProvider(ChatResponse(text="hello", stop_reason="end_turn"))
    provider = TracingProvider(mock_llm, trace)

    await provider.chat(messages=[{"role": "user", "content": "test"}], tool_schemas=[], system="test")

    await trace.stop()

    content = trace_file.read_text()
    assert "api_call" in content
    assert "api_response" in content
    assert "CORE→LLM" in content
    assert "LLM→CORE" in content

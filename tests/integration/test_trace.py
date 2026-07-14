import pytest
from pathlib import Path

from rcode.core.events.bus import EventBus
from rcode.core.llm.types import ChatResponse
from rcode.core.trace.provider import TracingProvider
from rcode.core.trace.record import TraceRecord
from rcode.core.trace.writer import TraceWriter


class MockLLMProvider:
    def __init__(self, response: ChatResponse):
        self._response = response

    async def chat(self, messages, tool_schemas, system):
        return self._response


@pytest.mark.asyncio
async def test_trace_full_flow(tmp_path):
    """测试完整的 Trace 流程。"""
    trace_file = tmp_path / "trace.jsonl"
    trace = TraceWriter(trace_file)
    await trace.start()

    # 模拟 LLM 调用
    mock_llm = MockLLMProvider(ChatResponse(text="hello", stop_reason="end_turn"))
    provider = TracingProvider(mock_llm, trace)

    await provider.chat(
        messages=[{"role": "user", "content": "test"}],
        tool_schemas=[],
        system="test",
    )

    await trace.stop()

    # 验证 trace 文件
    content = trace_file.read_text()
    assert "api_call" in content
    assert "api_response" in content
    assert "CORE→LLM" in content
    assert "LLM→CORE" in content


@pytest.mark.asyncio
async def test_trace_event_bus_integration(tmp_path):
    """测试 Trace 与 EventBus 集成。"""
    trace_file = tmp_path / "trace.jsonl"
    trace = TraceWriter(trace_file)
    await trace.start()

    bus = EventBus()
    bus.subscribe(trace.emit)

    # 发布事件
    from rcode.core.events.types import RunStartedEvent
    await bus.publish(RunStartedEvent(
        run_id="run_1",
        goal="test",
        ts="2026-07-14T10:00:00Z",
    ))

    await trace.stop()

    # 验证事件被记录
    content = trace_file.read_text()
    assert "run_1" in content
    assert "test" in content

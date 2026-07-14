import pytest
from unittest.mock import AsyncMock, MagicMock

from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.events.types import (
    RunFinishedEvent,
    RunStartedEvent,
    StepStartedEvent,
    ToolCallStartedEvent,
)
from rcode.core.llm.types import ChatResponse, ToolCall
from rcode.core.loop import AgentLoop
from rcode.core.tools.builtin.bash import BashTool
from rcode.core.tools.registry import ToolRegistry


class MockLLMProvider:
    def __init__(self, responses):
        self._responses = responses
        self._call_count = 0

    async def chat(self, messages, tool_schemas, system):
        if self._call_count < len(self._responses):
            resp = self._responses[self._call_count]
            self._call_count += 1
            return resp
        return ChatResponse(text="Done", stop_reason="end_turn")


@pytest.mark.asyncio
async def test_agent_loop_publishes_events():
    mock_llm = MockLLMProvider([
        ChatResponse(text="Hello!", stop_reason="end_turn"),
    ])
    registry = ToolRegistry()
    bus = EventBus()

    received_events = []

    async def capture_event(event):
        received_events.append(event)

    bus.subscribe(capture_event)

    loop = AgentLoop(mock_llm, registry, bus)
    context = ExecutionContext(goal="test", run_id="test_1")

    await loop.run(context)

    event_types = [e.type for e in received_events]
    assert "run.started" in event_types
    assert "run.finished" in event_types
    assert "step.started" in event_types
    assert "step.finished" in event_types


@pytest.mark.asyncio
async def test_agent_loop_tool_call_events():
    mock_llm = MockLLMProvider([
        ChatResponse(
            tool_calls=[ToolCall(id="1", name="bash", input={"command": "echo hi"})],
            stop_reason="tool_use",
        ),
        ChatResponse(text="Done", stop_reason="end_turn"),
    ])
    registry = ToolRegistry()
    registry.register(BashTool())
    bus = EventBus()

    received_events = []

    async def capture_event(event):
        received_events.append(event)

    bus.subscribe(capture_event)

    loop = AgentLoop(mock_llm, registry, bus)
    context = ExecutionContext(goal="test", run_id="test_2")

    await loop.run(context)

    event_types = [e.type for e in received_events]
    assert "tool.call_started" in event_types
    assert "tool.call_finished" in event_types

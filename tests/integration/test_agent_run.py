import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.llm.types import ChatResponse, ToolCall
from rcode.core.loop import AgentLoop
from rcode.core.runner import AgentRunner, RunOutcome
from rcode.core.tools.base import ToolResult
from rcode.core.tools.registry import ToolRegistry
from rcode.core.tools.builtin.bash import BashTool


class MockLLMProvider:
    """Mock LLM provider for testing."""

    def __init__(self, responses: list[ChatResponse]):
        self._responses = responses
        self._call_count = 0

    async def chat(self, messages, tool_schemas, system):
        if self._call_count < len(self._responses):
            resp = self._responses[self._call_count]
            self._call_count += 1
            return resp
        return ChatResponse(text="Done", stop_reason="end_turn")


@pytest.mark.asyncio
async def test_agent_loop_simple_task():
    """Test agent loop with a simple text response."""
    mock_llm = MockLLMProvider([
        ChatResponse(text="Hello!", stop_reason="end_turn"),
    ])
    registry = ToolRegistry()
    bus = EventBus()

    loop = AgentLoop(mock_llm, registry, bus)
    context = ExecutionContext(goal="Say hello", run_id="test_1")

    await loop.run(context)

    assert context.status == "success"
    assert context.result == "Hello!"


@pytest.mark.asyncio
async def test_agent_loop_with_tool_call():
    """Test agent loop with tool calls."""
    mock_llm = MockLLMProvider([
        ChatResponse(
            tool_calls=[ToolCall(id="1", name="bash", input={"command": "echo test"})],
            stop_reason="tool_use",
        ),
        ChatResponse(text="Task complete", stop_reason="end_turn"),
    ])
    registry = ToolRegistry()
    registry.register(BashTool())
    bus = EventBus()

    loop = AgentLoop(mock_llm, registry, bus)
    context = ExecutionContext(goal="Run echo", run_id="test_2")

    await loop.run(context)

    assert context.status == "success"
    assert context.result == "Task complete"
    assert context.step == 2


@pytest.mark.asyncio
async def test_agent_loop_max_steps():
    """Test agent loop stops at max steps."""
    infinite_responses = [
        ChatResponse(
            tool_calls=[ToolCall(id=str(i), name="bash", input={"command": "echo loop"})],
            stop_reason="tool_use",
        )
        for i in range(100)
    ]
    mock_llm = MockLLMProvider(infinite_responses)
    registry = ToolRegistry()
    registry.register(BashTool())
    bus = EventBus()

    loop = AgentLoop(mock_llm, registry, bus)
    context = ExecutionContext(goal="Loop forever", run_id="test_3", max_steps=3)

    await loop.run(context)

    assert context.status == "failed"
    assert context.result == "exceeded_max_steps"
    assert context.step == 3


@pytest.mark.asyncio
async def test_agent_runner_success():
    """Test AgentRunner with mock LLM."""
    mock_llm = MockLLMProvider([
        ChatResponse(
            tool_calls=[ToolCall(id="1", name="bash", input={"command": "echo hello"})],
            stop_reason="tool_use",
        ),
        ChatResponse(text="Done", stop_reason="end_turn"),
    ])

    with patch("rcode.core.runner.AnthropicProvider", return_value=mock_llm):
        runner = AgentRunner(MagicMock())
        outcome = await runner.run("Test goal")

    assert outcome.status == "success"
    assert outcome.result == "Done"


@pytest.mark.asyncio
async def test_agent_runner_error():
    """Test AgentRunner handles errors."""
    async def failing_chat(messages, tool_schemas, system):
        raise Exception("API error")

    mock_llm = MagicMock()
    mock_llm.chat = failing_chat

    with patch("rcode.core.runner.AnthropicProvider", return_value=mock_llm):
        runner = AgentRunner(MagicMock())
        outcome = await runner.run("Test goal")

    assert outcome.status == "failed"
    assert outcome.result == "llm_error"


@pytest.mark.asyncio
async def test_tool_result_in_context():
    """Test tool results are correctly added to context."""
    context = ExecutionContext(goal="test", run_id="test_4")

    # Add assistant message with tool call
    resp = ChatResponse(
        tool_calls=[ToolCall(id="1", name="bash", input={"command": "ls"})],
        stop_reason="tool_use",
    )
    context.add_assistant_message(resp)

    # Add tool result
    from rcode.core.tools.base import ToolResult
    result = ToolResult(content="file1.txt\nfile2.txt")
    context.add_tool_result("1", result)

    assert len(context.messages) == 3  # user + assistant + tool_result
    assert context.messages[1]["role"] == "assistant"
    assert context.messages[2]["role"] == "user"

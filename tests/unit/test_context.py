from rcode.core.context import ExecutionContext
from rcode.core.llm.types import ChatResponse, ToolCall
from rcode.core.tools.base import ToolResult


def test_context_init():
    ctx = ExecutionContext(goal="test goal", run_id="run_1")
    assert ctx.goal == "test goal"
    assert ctx.run_id == "run_1"
    assert ctx.step == 0
    assert ctx.status == "running"
    assert len(ctx.messages) == 1
    assert ctx.messages[0]["role"] == "user"
    assert ctx.messages[0]["content"] == "test goal"


def test_context_system_prompt():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    prompt = ctx.system_prompt()
    assert "AI assistant" in prompt
    assert "tools" in prompt


def test_context_add_assistant_message_text():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    resp = ChatResponse(text="hello", stop_reason="end_turn")
    ctx.add_assistant_message(resp)
    assert len(ctx.messages) == 2
    assert ctx.messages[1]["role"] == "assistant"


def test_context_add_assistant_message_tool_calls():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    tc = ToolCall(id="1", name="bash", input={"command": "ls"})
    resp = ChatResponse(tool_calls=[tc], stop_reason="tool_use")
    ctx.add_assistant_message(resp)
    assert len(ctx.messages) == 2
    content = ctx.messages[1]["content"]
    assert any(b.get("type") == "tool_use" for b in content)


def test_context_add_tool_result():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    result = ToolResult(content="output")
    ctx.add_tool_result("1", result)
    assert len(ctx.messages) == 2
    assert ctx.messages[1]["role"] == "user"


def test_context_is_done():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    assert ctx.is_done() is False


def test_context_mark_done():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    ctx.mark_done()
    assert ctx.is_done() is True
    assert ctx.status == "success"


def test_context_mark_failed():
    ctx = ExecutionContext(goal="test", run_id="run_1")
    ctx.mark_failed("error")
    assert ctx.is_done() is True
    assert ctx.status == "failed"
    assert ctx.result == "error"

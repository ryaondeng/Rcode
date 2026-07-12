from rcode.core.llm.types import ChatResponse, ToolCall


def test_tool_call():
    tc = ToolCall(id="1", name="bash", input={"command": "echo hello"})
    assert tc.id == "1"
    assert tc.name == "bash"
    assert tc.input == {"command": "echo hello"}


def test_chat_response_text():
    resp = ChatResponse(text="hello", stop_reason="end_turn")
    assert resp.text == "hello"
    assert resp.tool_calls == []
    assert resp.stop_reason == "end_turn"


def test_chat_response_tool_calls():
    tc = ToolCall(id="1", name="bash", input={"command": "ls"})
    resp = ChatResponse(tool_calls=[tc], stop_reason="tool_use")
    assert resp.text is None
    assert len(resp.tool_calls) == 1
    assert resp.stop_reason == "tool_use"


def test_chat_response_defaults():
    resp = ChatResponse()
    assert resp.text is None
    assert resp.tool_calls == []
    assert resp.stop_reason == "end_turn"

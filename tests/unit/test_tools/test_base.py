from rcode.core.tools.base import BaseTool, ToolResult


def test_tool_result_success():
    result = ToolResult(content="ok")
    assert result.content == "ok"
    assert result.is_error is False
    assert result.error_type is None


def test_tool_result_error():
    result = ToolResult(content="failed", is_error=True, error_type="timeout")
    assert result.content == "failed"
    assert result.is_error is True
    assert result.error_type == "timeout"

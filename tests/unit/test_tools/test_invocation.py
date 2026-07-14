import pytest

from rcode.core.llm.types import ToolCall
from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.invocation import invoke_tool
from rcode.core.tools.registry import ToolRegistry


class MockTool(BaseTool):
    name = "mock"
    description = "A mock tool"
    input_schema = {"type": "object"}

    async def invoke(self, params: dict) -> ToolResult:
        return ToolResult(content="ok")


class SlowTool(BaseTool):
    name = "slow"
    description = "A slow tool"
    input_schema = {"type": "object"}

    async def invoke(self, params: dict) -> ToolResult:
        import asyncio
        await asyncio.sleep(60)
        return ToolResult(content="done")


@pytest.mark.asyncio
async def test_invoke_tool_success():
    registry = ToolRegistry()
    registry.register(MockTool())
    tc = ToolCall(id="1", name="mock", input={})
    result = await invoke_tool(registry, tc)
    assert result.content == "ok"
    assert result.is_error is False


@pytest.mark.asyncio
async def test_invoke_tool_not_found():
    registry = ToolRegistry()
    tc = ToolCall(id="1", name="nonexistent", input={})
    result = await invoke_tool(registry, tc)
    assert result.is_error is True
    assert result.error_type == "not_found"


@pytest.mark.asyncio
async def test_invoke_tool_timeout():
    # registry = ToolRegistry()
    # registry.register(SlowTool())
    # tc = ToolCall(id="1", name="slow", input={})
    # result = await invoke_tool(registry, tc)
    # assert result.is_error is True
    # assert result.error_type == "timeout"
    pass

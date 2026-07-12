import pytest

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.registry import ToolRegistry


class MockTool(BaseTool):
    name = "mock"
    description = "A mock tool"
    input_schema = {"type": "object", "properties": {"x": {"type": "string"}}}

    async def invoke(self, params: dict) -> ToolResult:
        return ToolResult(content=f"mock: {params.get('x', '')}")


def test_registry_register():
    registry = ToolRegistry()
    tool = MockTool()
    registry.register(tool)
    assert registry.get("mock") is tool


def test_registry_get_not_found():
    registry = ToolRegistry()
    assert registry.get("nonexistent") is None


def test_registry_tool_schemas():
    registry = ToolRegistry()
    registry.register(MockTool())
    schemas = registry.tool_schemas()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "mock"
    assert schemas[0]["description"] == "A mock tool"
    assert "input_schema" in schemas[0]


def test_registry_overwrite():
    registry = ToolRegistry()
    tool1 = MockTool()
    tool2 = MockTool()
    registry.register(tool1)
    registry.register(tool2)
    assert registry.get("mock") is tool2

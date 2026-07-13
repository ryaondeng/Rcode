from __future__ import annotations

from rcode.core.tools.base import BaseTool


class ToolRegistry:
    """工具注册表，管理所有可用工具。

    职责：
    1. 注册和存储工具
    2. 按名称查找工具
    3. 生成工具 schema 列表（供 LLM 使用）
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """注册工具，同名覆盖。"""
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        """按名称查找工具，不存在返回 None。"""
        return self._tools.get(name)

    def tool_schemas(self) -> list[dict]:
        """返回所有工具的 Anthropic 格式 schema 列表。"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]

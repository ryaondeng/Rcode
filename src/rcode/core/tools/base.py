from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolResult:
    """工具执行结果。"""
    content: str  # 结果内容
    is_error: bool = False  # 是否错误
    error_type: str | None = None  # 错误类型："timeout" | "runtime_error" | "not_found"


class BaseTool(ABC):
    """工具基类，所有工具必须继承此类。

    子类需要实现：
    - name: 工具名称
    - description: 工具描述
    - input_schema: 输入参数 schema
    - invoke(): 执行工具逻辑
    """
    name: str
    description: str
    input_schema: dict

    @abstractmethod
    async def invoke(self, params: dict) -> ToolResult:
        """执行工具。

        Args:
            params: 工具参数

        Returns:
            ToolResult: 执行结果
        """
        ...

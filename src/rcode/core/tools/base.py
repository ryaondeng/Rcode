from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolResult:
    content: str
    is_error: bool = False
    error_type: str | None = None  # "timeout" | "runtime_error" | "not_found"


class BaseTool(ABC):
    name: str
    description: str
    input_schema: dict

    @abstractmethod
    async def invoke(self, params: dict) -> ToolResult:
        """Execute the tool with given parameters."""
        ...

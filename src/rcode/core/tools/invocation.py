from __future__ import annotations

import asyncio
import logging

from rcode.core.llm.types import ToolCall
from rcode.core.tools.base import ToolResult
from rcode.core.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

_TOOL_TIMEOUT = 30.0


async def invoke_tool(
    registry: ToolRegistry,
    tool_call: ToolCall,
) -> ToolResult:
    tool = registry.get(tool_call.name)
    if not tool:
        return ToolResult(
            content=f"Tool not found: {tool_call.name}",
            is_error=True,
            error_type="not_found",
        )

    try:
        return await asyncio.wait_for(
            tool.invoke(tool_call.input),
            timeout=_TOOL_TIMEOUT,
        )
    except asyncio.TimeoutError:
        logger.warning("Tool %s timed out", tool_call.name)
        return ToolResult(
            content="Tool execution timed out",
            is_error=True,
            error_type="timeout",
        )
    except Exception as e:
        logger.exception("Tool %s failed", tool_call.name)
        return ToolResult(
            content=str(e),
            is_error=True,
            error_type="runtime_error",
        )

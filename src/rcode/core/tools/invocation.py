from __future__ import annotations

import asyncio
import logging

from rcode.core.llm.types import ToolCall
from rcode.core.tools.base import ToolResult
from rcode.core.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

_TOOL_TIMEOUT = 30.0  # 工具执行超时时间（秒）


async def invoke_tool(
    registry: ToolRegistry,
    tool_call: ToolCall,
) -> ToolResult:
    """执行工具调用。

    流程：
    1. 从注册表中查找工具
    2. 如果工具不存在，返回错误
    3. 执行工具，设置超时保护
    4. 捕获异常并返回错误结果

    Args:
        registry: 工具注册表
        tool_call: 工具调用信息

    Returns:
        ToolResult: 工具执行结果
    """
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

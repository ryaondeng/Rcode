import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from rcode.core.loop import AgentLoop
from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.compact.budget import TokenBudget


# 功能：测试 AgentLoop 无 compactor 时不压缩
# 设计：compactor=None 时跳过水位检查
@pytest.mark.asyncio
async def test_agent_loop_no_compactor():
    bus = EventBus()
    provider = MagicMock()
    provider.chat = AsyncMock(return_value=MagicMock(
        stop_reason="end_turn",
        text="done",
        tool_calls=[],
    ))
    registry = MagicMock()
    registry.tool_schemas = MagicMock(return_value=[])

    loop = AgentLoop(provider, registry, bus)
    context = ExecutionContext(goal="test", run_id="123")

    await loop.run(context)
    assert context.status == "success"


# 功能：测试 AgentLoop threshold=0 时不压缩
# 设计：compact_threshold=0 时跳过水位检查
@pytest.mark.asyncio
async def test_agent_loop_threshold_zero():
    bus = EventBus()
    provider = MagicMock()
    provider.chat = AsyncMock(return_value=MagicMock(
        stop_reason="end_turn",
        text="done",
        tool_calls=[],
    ))
    registry = MagicMock()
    registry.tool_schemas = MagicMock(return_value=[])

    loop = AgentLoop(provider, registry, bus, compact_threshold=0.0)
    context = ExecutionContext(goal="test", run_id="123")

    await loop.run(context)
    assert context.status == "success"


# 功能：测试 AgentLoop 压缩失败不中断
# 设计：compactor 抛异常时主循环继续
@pytest.mark.asyncio
async def test_agent_loop_compact_failure():
    bus = EventBus()
    provider = MagicMock()
    provider.chat = AsyncMock(return_value=MagicMock(
        stop_reason="end_turn",
        text="done",
        tool_calls=[],
    ))
    registry = MagicMock()
    registry.tool_schemas = MagicMock(return_value=[])

    mock_compactor = MagicMock()
    mock_compactor.compact_messages = AsyncMock(side_effect=Exception("LLM error"))

    loop = AgentLoop(
        provider, registry, bus,
        compactor=mock_compactor,
        compact_threshold=0.0001,  # 低阈值触发压缩
    )
    # 添加长消息触发压缩
    context = ExecutionContext(goal="test", run_id="123")
    context.messages = [{"role": "user", "content": "x" * 1000}]

    await loop.run(context)
    # 压缩失败但主循环继续
    assert context.status == "success"

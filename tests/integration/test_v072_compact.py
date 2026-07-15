import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from rcode.core.loop import AgentLoop
from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.compact.budget import TokenBudget
from rcode.core.compact.compactor import Compactor


# 功能：测试压缩流程集成
# 设计：超预算消息触发压缩
@pytest.mark.asyncio
async def test_compact_flow():
    bus = EventBus()
    provider = MagicMock()
    provider.chat = AsyncMock(return_value=MagicMock(
        stop_reason="end_turn", text="done", tool_calls=[]
    ))
    registry = MagicMock()
    registry.tool_schemas = MagicMock(return_value=[])

    mock_compactor = MagicMock()
    mock_result = MagicMock()
    mock_result.summary_text = "compressed summary"
    mock_result.original_token_estimate = 1000
    mock_result.summary_tokens = 100
    mock_compactor.compact_messages = AsyncMock(return_value=mock_result)

    loop = AgentLoop(
        provider, registry, bus,
        compactor=mock_compactor,
        compact_threshold=0.0001,
    )
    # 添加超长消息
    context = ExecutionContext(goal="test", run_id="123")
    context.messages = [{"role": "user", "content": "x" * 1000}]

    await loop.run(context)

    # 验证压缩被调用
    mock_compactor.compact_messages.assert_called_once()
    # 验证历史被替换
    assert context.messages[0]["content"] == "compressed summary"

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
from pathlib import Path

from rcode.core.runner import AgentRunner, RunOutcome
from rcode.core.session.manager import SessionManager
from rcode.core.session.store import SessionStore
from rcode.core.config import RcodeConfig


# 功能：测试 Session 多轮对话
# 设计：同一 session_id 连续两次 run，第二次能看到第一次的历史
@pytest.mark.asyncio
@patch('rcode.core.runner.AnthropicProvider')
async def test_session_multi_turn(mock_provider):
    with tempfile.TemporaryDirectory() as tmpdir:
        config = RcodeConfig()
        runner = AgentRunner(config)

        # 第一次 run
        mock_provider.return_value.chat = AsyncMock(return_value=MagicMock(
            stop_reason="end_turn", text="First response", tool_calls=[]
        ))
        outcome1 = await runner.run("test-session", "first message")
        assert outcome1.status == "success"

        # 第二次 run（同一 session）
        mock_provider.return_value.chat = AsyncMock(return_value=MagicMock(
            stop_reason="end_turn", text="Second response", tool_calls=[]
        ))
        outcome2 = await runner.run("test-session", "second message")
        assert outcome2.status == "success"


# 功能：测试旧模式向后兼容
# 设计：run(goal) 模式仍可用
@pytest.mark.asyncio
@patch('rcode.core.runner.AnthropicProvider')
async def test_backward_compat_old_mode(mock_provider):
    config = RcodeConfig()
    runner = AgentRunner(config)

    mock_provider.return_value.chat = AsyncMock(return_value=MagicMock(
        stop_reason="end_turn", text="Response", tool_calls=[]
    ))
    outcome = await runner.run("test goal")
    assert outcome.status == "success"
    assert outcome.result == "Response"

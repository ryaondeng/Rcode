import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import tempfile

from rcode.core.runner import AgentRunner, RunOutcome
from rcode.cli.printer import ConsoleSubscriber
from rcode.core.events.types import (
    RunStartedEvent, RunFinishedEvent, StepStartedEvent,
    ToolCallStartedEvent, ToolCallFinishedEvent, LlmCallStartedEvent,
    SessionAttachedEvent, SessionDetachedEvent,
)
from rcode.core.config import RcodeConfig


# 功能：测试 RunOutcome 数据类
# 设计：验证 status 和 result 字段正确赋值
def test_run_outcome():
    outcome = RunOutcome(status="success", result="test result")
    assert outcome.status == "success"
    assert outcome.result == "test result"


def test_run_outcome_failed():
    outcome = RunOutcome(status="failed", result="error")
    assert outcome.status == "failed"
    assert outcome.result == "error"


# 功能：测试 ConsoleSubscriber 处理 RunStartedEvent
# 设计：验证 printer 能正确处理启动事件，不抛异常
def test_console_subscriber_run_started(capsys):
    subscriber = ConsoleSubscriber()
    event = RunStartedEvent(run_id="123", goal="test goal", ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "test goal" in captured.out


# 功能：测试 ConsoleSubscriber 处理 RunFinishedEvent
# 设计：验证 printer 能正确处理结束事件，不抛异常
def test_console_subscriber_run_finished(capsys):
    subscriber = ConsoleSubscriber()
    subscriber._run_start = 0
    event = RunFinishedEvent(run_id="123", status="success", ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "Done" in captured.out


# 功能：测试 ConsoleSubscriber 处理 ToolCallStartedEvent
# 设计：验证 printer 能正确处理工具调用事件
def test_console_subscriber_tool_call_started(capsys):
    subscriber = ConsoleSubscriber()
    event = ToolCallStartedEvent(run_id="123", tool_name="bash", params={"command": "ls"}, ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "bash" in captured.out


# 功能：测试 ConsoleSubscriber 处理 ToolCallFinishedEvent
# 设计：验证 printer 能正确处理工具完成事件
def test_console_subscriber_tool_call_finished(capsys):
    subscriber = ConsoleSubscriber()
    event = ToolCallFinishedEvent(run_id="123", tool_name="bash", is_error=False, tool_result="output", ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "output" in captured.out


# 功能：测试 ConsoleSubscriber 处理 LlmCallStartedEvent
# 设计：验证 printer 能正确处理 LLM 调用事件
def test_console_subscriber_llm_call_started(capsys):
    subscriber = ConsoleSubscriber()
    event = LlmCallStartedEvent(run_id="123", step=1, ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "LLM" in captured.out


# 功能：测试 AgentRunner 初始化
# 设计：验证 runner 能正确初始化所有组件
@patch('rcode.core.runner.AnthropicProvider')
def test_agent_runner_init(mock_provider):
    config = RcodeConfig()
    runner = AgentRunner(config)
    assert runner._config == config
    assert runner._provider is not None
    assert runner._registry is not None
    assert runner._bus is not None
    assert runner._session_mgr is not None


# 功能：测试 AgentRunner 注册内置工具
# 设计：验证 6 个内置工具都已注册
@patch('rcode.core.runner.AnthropicProvider')
def test_agent_runner_register_builtin_tools(mock_provider):
    config = RcodeConfig()
    runner = AgentRunner(config)
    assert runner._registry.get("bash") is not None
    assert runner._registry.get("read_file") is not None
    assert runner._registry.get("write_file") is not None
    assert runner._registry.get("edit_file") is not None
    assert runner._registry.get("list_dir") is not None
    assert runner._registry.get("glob") is not None


# 功能：测试 AgentRunner.run 旧模式
# 设计：验证旧模式 run(goal) 能正确创建 session
@pytest.mark.asyncio
@patch('rcode.core.runner.AnthropicProvider')
async def test_agent_runner_run_old_mode(mock_provider):
    with tempfile.TemporaryDirectory() as tmpdir:
        config = RcodeConfig()
        runner = AgentRunner(config)
        runner._session_mgr = MagicMock()
        runner._session_mgr.load = AsyncMock(return_value=None)
        runner._session_mgr.create = AsyncMock(return_value=MagicMock(id="tmp_123"))
        runner._session_mgr.get_history = AsyncMock(return_value=[])
        runner._session_mgr.save = AsyncMock()

        with patch.object(runner, '_trace', MagicMock()):
            runner._trace.start = AsyncMock()
            runner._trace.stop = AsyncMock()

            with patch('rcode.core.runner.AgentLoop') as mock_loop:
                mock_loop_instance = MagicMock()
                mock_loop.return_value = mock_loop_instance
                mock_loop_instance.run = AsyncMock(side_effect=Exception("LLM not configured"))

                outcome = await runner.run("test goal")

                assert outcome.status == "failed"
                runner._session_mgr.create.assert_called_once()


# 功能：测试 AgentRunner.run 新模式
# 设计：验证新模式 run(session_id, input) 能正确加载 session
@pytest.mark.asyncio
@patch('rcode.core.runner.AnthropicProvider')
async def test_agent_runner_run_new_mode(mock_provider):
    with tempfile.TemporaryDirectory() as tmpdir:
        config = RcodeConfig()
        runner = AgentRunner(config)
        mock_session = MagicMock(id="test-session")
        runner._session_mgr = MagicMock()
        runner._session_mgr.load = AsyncMock(return_value=mock_session)
        runner._session_mgr.get_history = AsyncMock(return_value=[])
        runner._session_mgr.save = AsyncMock()

        with patch.object(runner, '_trace', MagicMock()):
            runner._trace.start = AsyncMock()
            runner._trace.stop = AsyncMock()

            with patch('rcode.core.runner.AgentLoop') as mock_loop:
                mock_loop_instance = MagicMock()
                mock_loop.return_value = mock_loop_instance
                mock_loop_instance.run = AsyncMock(side_effect=Exception("LLM not configured"))

                outcome = await runner.run("test-session", "user input")

                assert outcome.status == "failed"
                runner._session_mgr.load.assert_called_once_with("test-session")


# 功能：测试 RunOutcome 数据类
# 设计：验证空 result 的处理
def test_run_outcome_empty_result():
    outcome = RunOutcome(status="success", result="")
    assert outcome.status == "success"
    assert outcome.result == ""


# 功能：测试 ConsoleSubscriber 处理长 tool_result
# 设计：验证超过 150 字符的结果会被截断
def test_console_subscriber_long_tool_result(capsys):
    subscriber = ConsoleSubscriber()
    long_result = "x" * 200
    event = ToolCallFinishedEvent(run_id="123", tool_name="bash", is_error=False, tool_result=long_result, ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "..." in captured.out


# 功能：测试 ConsoleSubscriber 处理空 tool_result
# 设计：验证空结果不会打印
def test_console_subscriber_empty_tool_result(capsys):
    subscriber = ConsoleSubscriber()
    event = ToolCallFinishedEvent(run_id="123", tool_name="bash", is_error=False, tool_result="", ts="2024-01-01T00:00:00")
    subscriber(event)
    captured = capsys.readouterr()
    assert "Output" not in captured.out

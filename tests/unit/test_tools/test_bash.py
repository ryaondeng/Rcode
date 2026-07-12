import pytest

from rcode.core.tools.builtin.bash import BashTool


@pytest.mark.asyncio
async def test_bash_success():
    tool = BashTool()
    result = await tool.invoke({"command": "echo hello"})
    assert result.content.strip() == "hello"
    assert result.is_error is False


@pytest.mark.asyncio
async def test_bash_empty_command():
    tool = BashTool()
    result = await tool.invoke({})
    assert result.is_error is True


@pytest.mark.asyncio
async def test_bash_error_output():
    tool = BashTool()
    result = await tool.invoke({"command": "ls /nonexistent_path_12345"})
    assert result.is_error is False  # ls error goes to stderr, merged
    assert "No such file" in result.content or "cannot access" in result.content

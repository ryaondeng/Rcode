import pytest
from pathlib import Path

from rcode.core.tools.builtin.read_file import ReadFileTool
from rcode.core.tools.builtin.write_file import WriteFileTool
from rcode.core.tools.builtin.edit_file import EditFileTool
from rcode.core.tools.builtin.list_dir import ListDirTool
from rcode.core.tools.builtin.glob import GlobTool


@pytest.mark.asyncio
async def test_file_write_read_cycle(tmp_path, monkeypatch):
    """测试写入后读取的完整流程。"""
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))

    write_tool = WriteFileTool()
    read_tool = ReadFileTool()

    # 写入文件
    result = await write_tool.invoke({"path": "test.txt", "content": "hello world"})
    assert result.is_error is False

    # 读取文件
    result = await read_tool.invoke({"path": "test.txt"})
    assert result.content == "hello world"
    assert result.is_error is False


@pytest.mark.asyncio
async def test_edit_then_read(tmp_path, monkeypatch):
    """测试编辑后读取的完整流程。"""
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))

    write_tool = WriteFileTool()
    edit_tool = EditFileTool()
    read_tool = ReadFileTool()

    # 创建文件
    await write_tool.invoke({"path": "test.txt", "content": "hello world"})

    # 编辑文件
    result = await edit_tool.invoke({"path": "test.txt", "old_text": "world", "new_text": "python"})
    assert result.is_error is False

    # 读取验证
    result = await read_tool.invoke({"path": "test.txt"})
    assert result.content == "hello python"


@pytest.mark.asyncio
async def test_list_dir_then_glob(tmp_path, monkeypatch):
    """测试列出目录后匹配文件的流程。"""
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))

    write_tool = WriteFileTool()
    list_tool = ListDirTool()
    glob_tool = GlobTool()

    # 创建文件
    await write_tool.invoke({"path": "test.py", "content": "print('hello')"})
    await write_tool.invoke({"path": "test.txt", "content": "hello"})

    # 列出目录
    result = await list_tool.invoke({})
    assert "test.py" in result.content
    assert "test.txt" in result.content

    # 匹配 .py 文件
    result = await glob_tool.invoke({"pattern": "*.py"})
    assert "test.py" in result.content
    assert "test.txt" not in result.content


@pytest.mark.asyncio
async def test_path_security_across_tools(tmp_path, monkeypatch):
    """测试路径安全在所有工具中生效。"""
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))

    read_tool = ReadFileTool()
    write_tool = WriteFileTool()
    edit_tool = EditFileTool()
    list_tool = ListDirTool()
    glob_tool = GlobTool()

    # 所有工具都应该拒绝路径逃逸
    for tool in [read_tool, write_tool, edit_tool, list_tool, glob_tool]:
        with pytest.raises(ValueError, match="Path escapes workspace"):
            if tool == write_tool:
                await tool.invoke({"path": "../../etc/passwd", "content": "test"})
            elif tool == edit_tool:
                await tool.invoke({"path": "../../etc/passwd", "old_text": "a", "new_text": "b"})
            elif tool == list_tool:
                await tool.invoke({"path": "../../etc"})
            elif tool == glob_tool:
                await tool.invoke({"pattern": "*", "path": "../../etc"})
            else:
                await tool.invoke({"path": "../../etc/passwd"})

import pytest
from pathlib import Path

from rcode.core.tools.builtin.list_dir import ListDirTool


@pytest.fixture
def test_dir(tmp_path):
    (tmp_path / "file1.txt").write_text("")
    (tmp_path / "file2.py").write_text("")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file3.txt").write_text("")
    return tmp_path


@pytest.mark.asyncio
async def test_list_dir_success(test_dir, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_dir))
    tool = ListDirTool()
    result = await tool.invoke({})
    assert "file1.txt" in result.content
    assert "file2.py" in result.content
    assert "subdir/" in result.content
    assert result.is_error is False


@pytest.mark.asyncio
async def test_list_dir_with_depth(test_dir, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_dir))
    tool = ListDirTool()
    result = await tool.invoke({"max_depth": 0})
    assert "file1.txt" in result.content
    assert "subdir/" in result.content
    assert "file3.txt" not in result.content  # 深度限制，不进入子目录


@pytest.mark.asyncio
async def test_list_dir_not_found(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = ListDirTool()
    result = await tool.invoke({"path": "nonexistent"})
    assert result.is_error is True


@pytest.mark.asyncio
async def test_list_dir_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = ListDirTool()
    result = await tool.invoke({})
    assert "empty" in result.content.lower()

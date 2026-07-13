import pytest
from pathlib import Path

from rcode.core.tools.builtin.write_file import WriteFileTool


@pytest.mark.asyncio
async def test_write_file_success(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = WriteFileTool()
    result = await tool.invoke({"path": "test.txt", "content": "hello"})
    assert result.is_error is False
    assert (tmp_path / "test.txt").read_text() == "hello"


@pytest.mark.asyncio
async def test_write_file_creates_parent_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = WriteFileTool()
    result = await tool.invoke({"path": "sub/dir/test.txt", "content": "hello"})
    assert result.is_error is False
    assert (tmp_path / "sub/dir/test.txt").read_text() == "hello"


@pytest.mark.asyncio
async def test_write_file_overwrites(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    (tmp_path / "test.txt").write_text("old")
    tool = WriteFileTool()
    result = await tool.invoke({"path": "test.txt", "content": "new"})
    assert result.is_error is False
    assert (tmp_path / "test.txt").read_text() == "new"

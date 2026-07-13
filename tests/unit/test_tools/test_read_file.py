import pytest
from pathlib import Path

from rcode.core.tools.builtin.read_file import ReadFileTool


@pytest.fixture
def test_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("line1\nline2\nline3\nline4\nline5")
    return file


@pytest.mark.asyncio
async def test_read_file_success(test_file, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_file.parent))
    tool = ReadFileTool()
    result = await tool.invoke({"path": "test.txt"})
    assert result.content == "line1\nline2\nline3\nline4\nline5"
    assert result.is_error is False


@pytest.mark.asyncio
async def test_read_file_with_limit(test_file, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_file.parent))
    tool = ReadFileTool()
    result = await tool.invoke({"path": "test.txt", "limit": 2})
    assert "line1\nline2" in result.content
    assert "3 more lines" in result.content


@pytest.mark.asyncio
async def test_read_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = ReadFileTool()
    result = await tool.invoke({"path": "nonexistent.txt"})
    assert result.is_error is True
    assert "not found" in result.content.lower()


@pytest.mark.asyncio
async def test_read_file_directory(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = ReadFileTool()
    result = await tool.invoke({"path": "."})
    assert result.is_error is True
    assert "directory" in result.content.lower()

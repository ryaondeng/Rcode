import pytest
from pathlib import Path

from rcode.core.tools.builtin.edit_file import EditFileTool


@pytest.fixture
def test_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world")
    return file


@pytest.mark.asyncio
async def test_edit_file_success(test_file, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_file.parent))
    tool = EditFileTool()
    result = await tool.invoke({"path": "test.txt", "old_text": "world", "new_text": "python"})
    assert result.is_error is False
    assert test_file.read_text() == "hello python"


@pytest.mark.asyncio
async def test_edit_file_only_first_occurrence(tmp_path, monkeypatch):
    file = tmp_path / "test.txt"
    file.write_text("aaa bbb aaa")
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = EditFileTool()
    result = await tool.invoke({"path": "test.txt", "old_text": "aaa", "new_text": "xxx"})
    assert result.is_error is False
    assert file.read_text() == "xxx bbb aaa"


@pytest.mark.asyncio
async def test_edit_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = EditFileTool()
    result = await tool.invoke({"path": "nonexistent.txt", "old_text": "a", "new_text": "b"})
    assert result.is_error is True


@pytest.mark.asyncio
async def test_edit_file_text_not_found(test_file, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_file.parent))
    tool = EditFileTool()
    result = await tool.invoke({"path": "test.txt", "old_text": "xyz", "new_text": "abc"})
    assert result.is_error is True
    assert "not found" in result.content.lower()

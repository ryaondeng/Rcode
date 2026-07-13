import pytest
from pathlib import Path

from rcode.core.tools.builtin.glob import GlobTool


@pytest.fixture
def test_dir(tmp_path):
    (tmp_path / "test.py").write_text("")
    (tmp_path / "test.txt").write_text("")
    (tmp_path / "sub.py").write_text("")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.py").write_text("")
    return tmp_path


@pytest.mark.asyncio
async def test_glob_py_files(test_dir, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_dir))
    tool = GlobTool()
    result = await tool.invoke({"pattern": "*.py"})
    assert "test.py" in result.content
    assert "sub.py" in result.content
    assert "test.txt" not in result.content
    assert result.is_error is False


@pytest.mark.asyncio
async def test_glob_recursive(test_dir, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_dir))
    tool = GlobTool()
    result = await tool.invoke({"pattern": "**/*.py"})
    assert "test.py" in result.content
    assert "nested.py" in result.content


@pytest.mark.asyncio
async def test_glob_no_match(tmp_path, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(tmp_path))
    tool = GlobTool()
    result = await tool.invoke({"pattern": "*.xyz"})
    assert "no files found" in result.content.lower()


@pytest.mark.asyncio
async def test_glob_with_path(test_dir, monkeypatch):
    monkeypatch.setenv("RCODE_WORKDIR", str(test_dir))
    tool = GlobTool()
    result = await tool.invoke({"pattern": "*.py", "path": "."})
    assert "test.py" in result.content

import pytest
from pathlib import Path

from rcode.core.tools.builtin.path_utils import safe_path, get_workdir


def test_safe_path_within_workdir():
    workdir = get_workdir()
    result = safe_path("test.txt")
    assert result.is_relative_to(workdir)


def test_safe_path_with_subdirectory():
    workdir = get_workdir()
    result = safe_path("subdir/test.txt")
    assert result.is_relative_to(workdir)


def test_safe_path_escape_raises():
    with pytest.raises(ValueError, match="Path escapes workspace"):
        safe_path("../../etc/passwd")


def test_safe_path_absolute_escape_raises():
    with pytest.raises(ValueError, match="Path escapes workspace"):
        safe_path("/etc/passwd")


def test_get_workdir_default():
    workdir = get_workdir()
    assert workdir.is_absolute()

import sys
from unittest.mock import patch

import pytest

from rcode.cli.main import main


def test_cli_version(capsys):
    with patch("sys.argv", ["rcode", "--version"]):
        try:
            main()
        except SystemExit:
            pass
    captured = capsys.readouterr()
    assert "rcode" in captured.out
    assert "0.1.0" in captured.out


def test_cli_no_command(capsys):
    with patch("sys.argv", ["rcode"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_ping_no_core(capsys):
    with patch("sys.argv", ["rcode", "ping"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_core_no_subcommand(capsys):
    with patch("sys.argv", ["rcode", "core"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

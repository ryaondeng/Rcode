import asyncio
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
    """测试 ping 命令在没有 Core 运行时的行为。

    如果 Core 正在运行，跳过此测试。
    """
    # 检查 Core 是否正在运行
    async def check_core():
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", 7437)
            writer.close()
            await writer.wait_closed()
            return True
        except (ConnectionRefusedError, OSError):
            return False

    if asyncio.run(check_core()):
        pytest.skip("Core is running, skipping test")

    with patch("sys.argv", ["rcode", "ping"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_core_no_subcommand(capsys):
    with patch("sys.argv", ["rcode", "core"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

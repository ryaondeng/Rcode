import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json

from rcode.ipc.client import IpcClient


# 功能：测试 IpcClient 初始化
# 设计：验证客户端能正确初始化
def test_ipc_client_init():
    client = IpcClient(host="127.0.0.1", port=7437)
    assert client._host == "127.0.0.1"
    assert client._port == 7437


# 功能：测试 IpcClient 连接
# 设计：验证客户端能正确连接
@pytest.mark.asyncio
async def test_ipc_client_connect():
    client = IpcClient()
    with patch('asyncio.open_connection') as mock_connect:
        mock_reader = AsyncMock()
        mock_writer = AsyncMock()
        mock_connect.return_value = (mock_reader, mock_writer)

        await client.connect()
        assert client._reader == mock_reader
        assert client._writer == mock_writer


# 功能：测试 IpcClient 关闭
# 设计：验证客户端能正确关闭
@pytest.mark.asyncio
async def test_ipc_client_close():
    client = IpcClient()
    mock_writer = AsyncMock()
    client._writer = mock_writer

    await client.close()
    mock_writer.close.assert_called_once()

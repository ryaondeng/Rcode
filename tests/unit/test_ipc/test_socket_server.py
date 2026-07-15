import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json

from rcode.core.transport.socket_server import SocketServer


# 功能：测试 SocketServer 初始化
# 设计：验证服务端能正确初始化
def test_socket_server_init():
    server = SocketServer(host="127.0.0.1", port=7437)
    assert server._host == "127.0.0.1"
    assert server._port == 7437
    assert server._handlers == {}


# 功能：测试 SocketServer 注册 handler
# 设计：验证 handler 能正确注册
def test_socket_server_register():
    server = SocketServer(host="127.0.0.1", port=7437)
    handler = AsyncMock()
    server.register("test.method", handler)
    assert "test.method" in server._handlers


# 功能：测试 SocketServer 处理 JSON-RPC 请求
# 设计：验证能正确解析和处理请求
@pytest.mark.asyncio
async def test_socket_server_handle_line():
    server = SocketServer(host="127.0.0.1", port=7437)
    handler = AsyncMock(return_value={"status": "ok"})
    server.register("test.method", handler)

    mock_writer = AsyncMock()
    request = {"jsonrpc": "2.0", "method": "test.method", "params": {}, "id": "1"}
    line = json.dumps(request).encode() + b"\n"

    await server._handle_line(line, mock_writer)

    handler.assert_called_once_with({})
    mock_writer.write.assert_called_once()

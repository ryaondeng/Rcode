import asyncio

import pytest

from rcode.core.transport.socket_client import SocketClient, ServerError
from rcode.core.transport.socket_server import SocketServer


async def _ping_handler(params: dict) -> dict:
    return {"pong": True, "client": params.get("client", "unknown")}


async def _error_handler(params: dict) -> dict:
    raise ValueError("test error")


async def _handler_error_handler(params: dict) -> dict:
    from rcode.core.bus.envelope import HandlerError
    raise HandlerError(-32600, "custom error", {"detail": "test"})


@pytest.mark.asyncio
async def test_ping_pong(free_port: int):
    server = SocketServer("127.0.0.1", free_port)
    server.register("core.ping", _ping_handler)
    await server.start()

    try:
        client = SocketClient("127.0.0.1", free_port)
        result = await client.send("core.ping", {"client": "test"})
        assert result["pong"] is True
        assert result["client"] == "test"
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_multiple_pings(free_port: int):
    server = SocketServer("127.0.0.1", free_port)
    server.register("core.ping", _ping_handler)
    await server.start()

    try:
        client = SocketClient("127.0.0.1", free_port)
        for i in range(5):
            result = await client.send("core.ping", {"client": f"client_{i}"})
            assert result["pong"] is True
            assert result["client"] == f"client_{i}"
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_method_not_found(free_port: int):
    server = SocketServer("127.0.0.1", free_port)
    await server.start()

    try:
        client = SocketClient("127.0.0.1", free_port)
        with pytest.raises(ServerError) as exc_info:
            await client.send("nonexistent.method")
        assert exc_info.value.code == -32601
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_handler_exception(free_port: int):
    server = SocketServer("127.0.0.1", free_port)
    server.register("test.error", _error_handler)
    await server.start()

    try:
        client = SocketClient("127.0.0.1", free_port)
        with pytest.raises(ServerError) as exc_info:
            await client.send("test.error")
        assert exc_info.value.code == -32603
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_handler_error_exception(free_port: int):
    server = SocketServer("127.0.0.1", free_port)
    server.register("test.handler_error", _handler_error_handler)
    await server.start()

    try:
        client = SocketClient("127.0.0.1", free_port)
        with pytest.raises(ServerError) as exc_info:
            await client.send("test.handler_error")
        assert exc_info.value.code == -32600
        assert exc_info.value.data == {"detail": "test"}
    finally:
        await server.stop()

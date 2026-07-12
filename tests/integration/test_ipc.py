import asyncio

import pytest

from rcode.core.transport.socket_client import SocketClient
from rcode.core.transport.socket_server import SocketServer


async def _ping_handler(params: dict) -> dict:
    return {"pong": True, "client": params.get("client", "unknown")}


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

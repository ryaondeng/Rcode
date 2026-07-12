from __future__ import annotations

import json
import uuid
from typing import Any

from pydantic import BaseModel, ValidationError

from rcode.core.bus.envelope import (
    INVALID_REQUEST,
    INTERNAL_ERROR,
    JsonRpcRequest,
    JsonRpcSuccess,
    make_error,
)


class SocketClient:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    async def send(self, method: str, params: dict[str, Any] | None = None) -> Any:
        import asyncio

        reader, writer = await asyncio.open_connection(self._host, self._port)
        try:
            req = JsonRpcRequest(
                id=str(uuid.uuid4()),
                method=method,
                params=params or {},
            )
            writer.write(req.model_dump_json().encode() + b"\n")
            await writer.drain()

            line = await reader.readline()
            if not line:
                raise ConnectionError("Server closed connection")

            raw: Any = json.loads(line)
            resp = JsonRpcSuccess.model_validate(raw)
            return resp.result
        finally:
            writer.close()
            await writer.wait_closed()

from __future__ import annotations

import json
import uuid
from typing import Any

from pydantic import BaseModel, ValidationError

from rcode.core.bus.envelope import (
    INVALID_REQUEST,
    INTERNAL_ERROR,
    JsonRpcError,
    JsonRpcRequest,
    JsonRpcSuccess,
    make_error,
)


class SocketClient:
    def __init__(self, host: str, port: int, timeout: float = 30.0) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout

    async def send(self, method: str, params: dict[str, Any] | None = None) -> Any:
        import asyncio

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(self._host, self._port),
            timeout=self._timeout,
        )
        try:
            req = JsonRpcRequest(
                id=str(uuid.uuid4()),
                method=method,
                params=params or {},
            )
            writer.write(req.model_dump_json().encode() + b"\n")
            await writer.drain()

            line = await asyncio.wait_for(reader.readline(), timeout=self._timeout)
            if not line:
                raise ConnectionError("Server closed connection")

            raw: Any = json.loads(line)

            if "error" in raw:
                error_resp = JsonRpcError.model_validate(raw)
                raise ServerError(
                    error_resp.error.code,
                    error_resp.error.message,
                    error_resp.error.data,
                )

            resp = JsonRpcSuccess.model_validate(raw)
            return resp.result
        finally:
            writer.close()
            await writer.wait_closed()


class ServerError(Exception):
    def __init__(self, code: int, message: str, data: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from typing import Any

logger = logging.getLogger(__name__)


class IpcClient:
    """JSON-RPC 客户端。"""

    def __init__(self, host: str = "127.0.0.1", port: int = 7437) -> None:
        self._host = host
        self._port = port
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        """连接到 Core 进程。"""
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port
        )

    async def close(self) -> None:
        """关闭连接。"""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

    async def call(self, method: str, **params) -> dict:
        """发送 JSON-RPC 请求。"""
        if not self._writer:
            await self.connect()

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(uuid.uuid4()),
        }

        self._writer.write(json.dumps(request).encode() + b"\n")
        await self._writer.drain()

        line = await self._reader.readline()
        return json.loads(line.decode())

    async def wait_for_result(self, run_id: str, timeout: float = 300) -> dict:
        """等待 run 完成。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                line = await asyncio.wait_for(
                    self._reader.readline(),
                    timeout=deadline - time.monotonic(),
                )
                data = json.loads(line.decode())
                if data.get("method") == "core.run.completed":
                    params = data.get("params", {})
                    if params.get("run_id") == run_id:
                        return params
            except asyncio.TimeoutError:
                break

        raise TimeoutError(f"Run {run_id} timed out")

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TraceWriter:
    """Trace 写入器，异步写入 JSONL 文件。"""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._queue: asyncio.Queue[BaseModel] = asyncio.Queue()
        self._task: asyncio.Task | None = None
        self._file = None

    async def start(self) -> None:
        """启动后台写入任务。"""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._file = open(self._path, "a", encoding="utf-8")
        self._task = asyncio.create_task(self._drain())

    async def stop(self) -> None:
        """停止后台任务，等待队列清空。"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        # 等待队列清空
        while not self._queue.empty():
            record = await self._queue.get()
            try:
                self._file.write(record.model_dump_json() + "\n")
                self._file.flush()
            except Exception as e:
                logger.warning("Failed to write trace record: %s", e)
        if self._file:
            self._file.close()

    def emit(self, record: BaseModel) -> None:
        """非阻塞写入，放入队列。"""
        self._queue.put_nowait(record)

    async def _drain(self) -> None:
        """后台协程，从队列读取并写入文件。"""
        while True:
            record = await self._queue.get()
            try:
                self._file.write(record.model_dump_json() + "\n")
                self._file.flush()
            except Exception as e:
                logger.warning("Failed to write trace record: %s", e)

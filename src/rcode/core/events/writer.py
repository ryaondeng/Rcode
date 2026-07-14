from __future__ import annotations

import logging
from pathlib import Path

from pydantic import BaseModel

from rcode.core.events.bus import EventBus

logger = logging.getLogger(__name__)


class EventWriter:
    """事件写入器，将事件持久化到 JSONL 文件。"""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._file = None

    async def __aenter__(self) -> EventWriter:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._file = open(self._path, "a", encoding="utf-8")
        return self

    async def __aexit__(self, *args) -> None:
        if self._file:
            self._file.close()

    async def handle(self, event: BaseModel) -> None:
        """处理事件，写入 JSONL 文件。"""
        try:
            self._file.write(event.model_dump_json() + "\n")
            self._file.flush()
        except Exception as e:
            logger.warning("Failed to write event: %s", e)

    def subscribe(self, bus: EventBus) -> None:
        """将自身注册为 EventBus 的订阅者。"""
        bus.subscribe(self.handle)

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from rcode.core.events.bus import EventBus
from rcode.core.trace.record import TraceRecord
from rcode.core.trace.writer import TraceWriter

logger = logging.getLogger(__name__)


class TraceEventSubscriber:
    """将 EventBus 事件转换为 TraceRecord 写入 Trace。"""

    def __init__(self, trace: TraceWriter) -> None:
        self._trace = trace

    def __call__(self, event: BaseModel) -> None:
        """处理事件，转换为 TraceRecord 并写入。"""
        from rcode.core.events.types import (
            RunStartedEvent, RunFinishedEvent,
            StepStartedEvent, StepFinishedEvent,
            ToolCallStartedEvent, ToolCallFinishedEvent,
            LlmCallStartedEvent, LlmCallFinishedEvent,
        )

        # 映射事件类型到 TraceRecord kind
        kind_map = {
            RunStartedEvent: "run.started",
            RunFinishedEvent: "run.finished",
            StepStartedEvent: "step.started",
            StepFinishedEvent: "step.finished",
            ToolCallStartedEvent: "tool.call_started",
            ToolCallFinishedEvent: "tool.call_finished",
            LlmCallStartedEvent: "llm.call_started",
            LlmCallFinishedEvent: "llm.call_finished",
        }

        event_type = type(event)
        kind = kind_map.get(event_type, event_type.__name__)

        # 提取公共字段
        data = event.model_dump()
        run_id = data.pop("run_id", None)
        ts = data.pop("ts", datetime.now().isoformat())

        self._trace.emit(TraceRecord(
            ts=ts,
            direction="CORE",
            layer="event",
            kind=kind,
            run_id=run_id,
            data=data,
        ))


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

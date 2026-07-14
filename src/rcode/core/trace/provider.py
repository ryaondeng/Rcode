from __future__ import annotations

import time
from datetime import UTC, datetime

from rcode.core.llm.base import LLMProvider
from rcode.core.llm.types import ChatResponse
from rcode.core.trace.record import TraceRecord
from rcode.core.trace.writer import TraceWriter


def _now() -> str:
    return datetime.now(UTC).isoformat()


class TracingProvider(LLMProvider):
    """装饰器模式，包裹真实 LLMProvider，记录追踪信息。"""

    def __init__(self, provider: LLMProvider, trace: TraceWriter) -> None:
        self._provider = provider
        self._trace = trace

    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        # 记录 LLM 调用开始
        self._trace.emit(TraceRecord(
            ts=_now(),
            direction="CORE→LLM",
            layer="llm",
            kind="api_call",
            data={"messages_count": len(messages)},
        ))

        t0 = time.monotonic()
        response = await self._provider.chat(messages, tool_schemas, system)
        latency_ms = int((time.monotonic() - t0) * 1000)

        # 记录 LLM 调用结束
        self._trace.emit(TraceRecord(
            ts=_now(),
            direction="LLM→CORE",
            layer="llm",
            kind="api_response",
            data={
                "stop_reason": response.stop_reason,
                "has_text": response.text is not None,
                "tool_calls_count": len(response.tool_calls),
                "latency_ms": latency_ms,
            },
        ))

        return response

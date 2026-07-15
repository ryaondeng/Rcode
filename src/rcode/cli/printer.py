from __future__ import annotations

import time
from datetime import datetime

from pydantic import BaseModel


class ConsoleSubscriber:
    """终端事件打印，从 runner.py 的 _EventPrinter 挪出。"""

    def __init__(self) -> None:
        self._run_start = 0
        self._step = 0

    def __call__(self, event: BaseModel) -> None:
        from rcode.core.events.types import (
            RunStartedEvent, RunFinishedEvent,
            StepStartedEvent,
            ToolCallStartedEvent, ToolCallFinishedEvent,
            LlmCallStartedEvent,
        )

        now = datetime.now().strftime("%H:%M:%S")

        if isinstance(event, RunStartedEvent):
            self._run_start = time.monotonic()
            print(f"Task: {event.goal}\n")

        elif isinstance(event, StepStartedEvent):
            self._step = event.step

        elif isinstance(event, LlmCallStartedEvent):
            print(f"{now} | Step {event.step} | [LLM] chat | ...")

        elif isinstance(event, ToolCallStartedEvent):
            args_str = str(event.params)[:50] if event.params else ""
            print(f"{now} | [Tool] {event.tool_name} | ... | Args: {args_str}")

        elif isinstance(event, ToolCallFinishedEvent):
            if event.tool_result:
                display = event.tool_result[:150]
                if len(event.tool_result) > 150:
                    display += "..."
                print(f"{now} | Output: {display}")

        elif isinstance(event, RunFinishedEvent):
            elapsed = time.monotonic() - self._run_start
            print(f"\nDone ({elapsed:.2f}s)")

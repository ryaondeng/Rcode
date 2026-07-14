from __future__ import annotations

import logging
from datetime import datetime

from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.events.types import (
    LlmCallFinishedEvent,
    LlmCallStartedEvent,
    RunFinishedEvent,
    RunStartedEvent,
    StepFinishedEvent,
    StepStartedEvent,
    ToolCallFinishedEvent,
    ToolCallStartedEvent,
)
from rcode.core.llm.base import LLMProvider
from rcode.core.tools.invocation import invoke_tool
from rcode.core.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now().isoformat()


class AgentLoop:
    """Agent 核心循环，驱动 Think → Act → Observe 过程。"""

    def __init__(
        self,
        provider: LLMProvider,
        registry: ToolRegistry,
        bus: EventBus,
    ) -> None:
        self._provider = provider
        self._registry = registry
        self._bus = bus

    async def run(self, context: ExecutionContext) -> None:
        """执行 Agent 循环。"""
        await self._bus.publish(RunStartedEvent(
            run_id=context.run_id,
            goal=context.goal,
            ts=_now(),
        ))

        while not context.is_done():
            if context.step >= context.max_steps:
                context.mark_failed("exceeded_max_steps")
                break

            context.step += 1
            await self._bus.publish(StepStartedEvent(
                run_id=context.run_id,
                step=context.step,
                ts=_now(),
            ))

            # Plan: call LLM
            await self._bus.publish(LlmCallStartedEvent(
                run_id=context.run_id,
                step=context.step,
                ts=_now(),
            ))

            try:
                response = await self._provider.chat(
                    messages=context.messages,
                    tool_schemas=self._registry.tool_schemas(),
                    system=context.system_prompt(),
                )
            except Exception:
                logger.exception("LLM call failed at step %d", context.step)
                context.mark_failed("llm_error")
                break

            await self._bus.publish(LlmCallFinishedEvent(
                run_id=context.run_id,
                step=context.step,
                stop_reason=response.stop_reason,
                ts=_now(),
            ))

            # Observe: add assistant message
            context.add_assistant_message(response)

            # Act: execute tool calls
            if response.stop_reason == "tool_use":
                for tool_call in response.tool_calls:
                    await self._bus.publish(ToolCallStartedEvent(
                        run_id=context.run_id,
                        tool_name=tool_call.name,
                        params=tool_call.input,
                        ts=_now(),
                    ))

                    result = await invoke_tool(self._registry, tool_call)
                    context.add_tool_result(tool_call.id, result)

                    await self._bus.publish(ToolCallFinishedEvent(
                        run_id=context.run_id,
                        tool_name=tool_call.name,
                        is_error=result.is_error,
                        tool_result=result.content[:500] if result.content else "",
                        ts=_now(),
                    ))

            elif response.stop_reason == "end_turn":
                context.mark_done()
                context.result = response.text
                if response.text:
                    await self._bus.publish(ToolCallFinishedEvent(
                        run_id=context.run_id,
                        tool_name="",
                        is_error=False,
                        tool_result=response.text[:500],
                        ts=_now(),
                    ))

            await self._bus.publish(StepFinishedEvent(
                run_id=context.run_id,
                step=context.step,
                ts=_now(),
            ))

        await self._bus.publish(RunFinishedEvent(
            run_id=context.run_id,
            status=context.status,
            ts=_now(),
        ))

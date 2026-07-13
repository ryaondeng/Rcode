from __future__ import annotations

import logging

from rcode.core.context import ExecutionContext
from rcode.core.llm.base import LLMProvider
from rcode.core.tools.invocation import invoke_tool
from rcode.core.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class AgentLoop:
    """Agent 核心循环，驱动 Think → Act → Observe 过程。

    负责：
    1. 调用 LLM 获取思考结果
    2. 执行工具调用
    3. 将结果回填到上下文
    4. 重复直到任务完成或达到步数限制
    """

    def __init__(
        self,
        provider: LLMProvider,
        registry: ToolRegistry,
    ) -> None:
        self._provider = provider
        self._registry = registry

    async def run(self, context: ExecutionContext) -> None:
        """执行 Agent 循环。

        循环流程：
        1. 检查步数限制
        2. 调用 LLM（Plan）
        3. 将回复添加到上下文（Observe）
        4. 执行工具调用（Act）
        5. 重复直到任务完成

        终止条件：
        - stop_reason == "end_turn"：LLM 认为任务完成
        - step >= max_steps：达到步数限制
        - LLM 调用异常：标记失败并退出
        """
        while not context.is_done():
            # Check max steps
            if context.step >= context.max_steps:
                context.mark_failed("exceeded_max_steps")
                break

            context.step += 1
            logger.debug("Step %d/%d", context.step, context.max_steps)

            # Plan: call LLM
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

            # Observe: add assistant message
            context.add_assistant_message(response)

            # Act: execute tool calls
            if response.stop_reason == "tool_use":
                for tool_call in response.tool_calls:
                    result = await invoke_tool(self._registry, tool_call)
                    context.add_tool_result(tool_call.id, result)
                    logger.debug(
                        "Tool %s: %s",
                        tool_call.name,
                        "error" if result.is_error else "success",
                    )
            elif response.stop_reason == "end_turn":
                context.mark_done()
                context.result = response.text
            elif context.step >= context.max_steps:
                context.mark_failed("exceeded_max_steps")
                break

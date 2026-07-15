from __future__ import annotations

from dataclasses import dataclass, field

from rcode.core.llm.types import ChatResponse
from rcode.core.tools.base import ToolResult


@dataclass
class ExecutionContext:
    """执行上下文，管理 Agent 运行状态。

    核心职责：
    1. 维护消息历史（messages）
    2. 跟踪执行状态（status）
    3. 管理系统提示词（system_prompt）
    4. 处理助手消息和工具结果的添加

    状态机：
    - running：执行中
    - success：任务完成
    - failed：执行失败
    """

    goal: str  # 用户目标
    run_id: str  # 运行 ID
    max_steps: int = 20  # 最大步数限制
    messages: list[dict] = field(default_factory=list)  # 消息历史
    step: int = 0  # 当前步数
    status: str = "running"  # 执行状态
    result: str | None = None  # 最终结果
    _is_done: bool = False  # 内部完成标志

    def __post_init__(self):
        if not self.messages:
            self.messages = [{"role": "user", "content": self.goal}]

    def system_prompt(self) -> str:
        return (
            "You are a helpful AI assistant. "
            "Use the available tools to complete the user's goal. "
            "When the goal is fully achieved, respond with a final answer "
            "and do not call any more tools."
        )

    def add_assistant_message(self, response: ChatResponse) -> None:
        blocks = []
        if response.text:
            blocks.append({"type": "text", "text": response.text})
        for tc in response.tool_calls:
            blocks.append(
                {"type": "tool_use", "id": tc.id, "name": tc.name, "input": tc.input}
            )
        self.messages.append({"role": "assistant", "content": blocks})

    def add_tool_result(self, tool_use_id: str, result: ToolResult) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result.content,
                        "is_error": result.is_error,
                    }
                ],
            }
        )

    def is_done(self) -> bool:
        return self._is_done or self.status != "running"

    def mark_done(self) -> None:
        self._is_done = True
        self.status = "success"

    def mark_failed(self, reason: str) -> None:
        self._is_done = True
        self.status = "failed"
        self.result = reason

    def replace_history(self, summary: str) -> None:
        """用摘要替换 runtime 中的旧 messages。

        原始 messages 仍完整保留在 Session store。
        """
        self.messages = [
            {"role": "user", "content": summary},
        ]

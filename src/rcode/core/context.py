from __future__ import annotations

from dataclasses import dataclass, field

from rcode.core.llm.types import ChatResponse
from rcode.core.tools.base import ToolResult


@dataclass
class ExecutionContext:
    goal: str
    run_id: str
    max_steps: int = 20
    messages: list[dict] = field(default_factory=list)
    step: int = 0
    status: str = "running"  # "running" | "success" | "failed"
    result: str | None = None
    _is_done: bool = False

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

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator


# Run 生命周期事件
class RunStartedEvent(BaseModel):
    """Run 开始事件。"""
    type: Literal["run.started"] = "run.started"
    run_id: str
    goal: str
    ts: str


class RunFinishedEvent(BaseModel):
    """Run 结束事件。"""
    type: Literal["run.finished"] = "run.finished"
    run_id: str
    status: str  # "success" | "failed"
    ts: str


# Step 生命周期事件
class StepStartedEvent(BaseModel):
    """Step 开始事件。"""
    type: Literal["step.started"] = "step.started"
    run_id: str
    step: int
    ts: str


class StepFinishedEvent(BaseModel):
    """Step 结束事件。"""
    type: Literal["step.finished"] = "step.finished"
    run_id: str
    step: int
    ts: str


# 工具调用事件
class ToolCallStartedEvent(BaseModel):
    """工具调用开始事件。"""
    type: Literal["tool.call_started"] = "tool.call_started"
    run_id: str
    tool_name: str
    params: dict
    ts: str


class ToolCallFinishedEvent(BaseModel):
    """工具调用结束事件。"""
    type: Literal["tool.call_finished"] = "tool.call_finished"
    run_id: str
    tool_name: str
    is_error: bool
    tool_result: str = ""
    ts: str


# LLM 监控事件
class LlmCallStartedEvent(BaseModel):
    """LLM 调用开始事件。"""
    type: Literal["llm.call_started"] = "llm.call_started"
    run_id: str
    step: int
    ts: str


class LlmCallFinishedEvent(BaseModel):
    """LLM 调用结束事件。"""
    type: Literal["llm.call_finished"] = "llm.call_finished"
    run_id: str
    step: int
    stop_reason: str
    ts: str


# 事件联合类型
Event = Annotated[
    RunStartedEvent
    | RunFinishedEvent
    | StepStartedEvent
    | StepFinishedEvent
    | ToolCallStartedEvent
    | ToolCallFinishedEvent
    | LlmCallStartedEvent
    | LlmCallFinishedEvent,
    Discriminator("type"),
]

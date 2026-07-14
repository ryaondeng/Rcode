from rcode.core.events.types import (
    RunStartedEvent,
    RunFinishedEvent,
    StepStartedEvent,
    StepFinishedEvent,
    ToolCallStartedEvent,
    ToolCallFinishedEvent,
    LlmCallStartedEvent,
    LlmCallFinishedEvent,
)


def test_run_started_event():
    event = RunStartedEvent(run_id="run_1", goal="test", ts="2026-07-13T10:00:00Z")
    data = event.model_dump()
    assert data["type"] == "run.started"
    assert data["run_id"] == "run_1"
    assert data["goal"] == "test"


def test_run_finished_event():
    event = RunFinishedEvent(run_id="run_1", status="success", ts="2026-07-13T10:00:00Z")
    data = event.model_dump()
    assert data["type"] == "run.finished"
    assert data["status"] == "success"


def test_step_started_event():
    event = StepStartedEvent(run_id="run_1", step=1, ts="2026-07-13T10:00:00Z")
    data = event.model_dump()
    assert data["type"] == "step.started"
    assert data["step"] == 1


def test_step_finished_event():
    event = StepFinishedEvent(run_id="run_1", step=1, ts="2026-07-13T10:00:00Z")
    data = event.model_dump()
    assert data["type"] == "step.finished"


def test_tool_call_started_event():
    event = ToolCallStartedEvent(
        run_id="run_1",
        tool_name="bash",
        params={"command": "echo hello"},
        ts="2026-07-13T10:00:00Z",
    )
    data = event.model_dump()
    assert data["type"] == "tool.call_started"
    assert data["tool_name"] == "bash"
    assert data["params"] == {"command": "echo hello"}


def test_tool_call_finished_event():
    event = ToolCallFinishedEvent(
        run_id="run_1",
        tool_name="bash",
        is_error=False,
        ts="2026-07-13T10:00:00Z",
    )
    data = event.model_dump()
    assert data["type"] == "tool.call_finished"
    assert data["is_error"] is False


def test_llm_call_started_event():
    event = LlmCallStartedEvent(run_id="run_1", step=1, ts="2026-07-13T10:00:00Z")
    data = event.model_dump()
    assert data["type"] == "llm.call_started"
    assert data["step"] == 1


def test_llm_call_finished_event():
    event = LlmCallFinishedEvent(
        run_id="run_1",
        step=1,
        stop_reason="end_turn",
        ts="2026-07-13T10:00:00Z",
    )
    data = event.model_dump()
    assert data["type"] == "llm.call_finished"
    assert data["stop_reason"] == "end_turn"

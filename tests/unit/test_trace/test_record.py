from rcode.core.trace.record import TraceRecord


def test_trace_record_serialization():
    record = TraceRecord(
        ts="2026-07-14T10:00:00Z",
        direction="CORE→LLM",
        layer="llm",
        kind="api_call",
        run_id="run_1",
        step=1,
        data={"messages_count": 5},
    )
    data = record.model_dump()
    assert data["ts"] == "2026-07-14T10:00:00Z"
    assert data["direction"] == "CORE→LLM"
    assert data["layer"] == "llm"
    assert data["kind"] == "api_call"
    assert data["run_id"] == "run_1"
    assert data["step"] == 1
    assert data["data"] == {"messages_count": 5}


def test_trace_record_defaults():
    record = TraceRecord(
        ts="2026-07-14T10:00:00Z",
        direction="CORE",
        layer="event",
        kind="event",
    )
    assert record.run_id is None
    assert record.step is None
    assert record.client_id is None
    assert record.data == {}

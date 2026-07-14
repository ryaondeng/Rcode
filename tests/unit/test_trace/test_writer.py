import pytest

from rcode.core.trace.record import TraceRecord
from rcode.core.trace.writer import TraceWriter


@pytest.mark.asyncio
async def test_trace_writer_write(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    writer = TraceWriter(trace_file)

    await writer.start()
    writer.emit(TraceRecord(
        ts="2026-07-14T10:00:00Z",
        direction="CORE→LLM",
        layer="llm",
        kind="api_call",
    ))
    await writer.stop()

    content = trace_file.read_text()
    assert "api_call" in content
    assert "CORE→LLM" in content


@pytest.mark.asyncio
async def test_trace_writer_multiple_records(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    writer = TraceWriter(trace_file)

    await writer.start()
    for i in range(3):
        writer.emit(TraceRecord(
            ts="2026-07-14T10:00:00Z",
            direction="CORE",
            layer="event",
            kind=f"event_{i}",
        ))
    await writer.stop()

    lines = trace_file.read_text().strip().split("\n")
    assert len(lines) == 3

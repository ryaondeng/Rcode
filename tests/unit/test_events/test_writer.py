import pytest
from pathlib import Path

from rcode.core.events.bus import EventBus
from rcode.core.events.types import RunStartedEvent
from rcode.core.events.writer import EventWriter


@pytest.mark.asyncio
async def test_event_writer_persistence(tmp_path):
    events_file = tmp_path / "events.jsonl"
    bus = EventBus()

    async with EventWriter(events_file) as writer:
        writer.subscribe(bus)
        await bus.publish(RunStartedEvent(
            run_id="run_1",
            goal="test",
            ts="2026-07-13T10:00:00Z",
        ))

    content = events_file.read_text()
    assert "run_1" in content
    assert "test" in content


@pytest.mark.asyncio
async def test_event_writer_multiple_events(tmp_path):
    events_file = tmp_path / "events.jsonl"
    bus = EventBus()

    async with EventWriter(events_file) as writer:
        writer.subscribe(bus)
        for i in range(3):
            await bus.publish(RunStartedEvent(
                run_id=f"run_{i}",
                goal=f"test_{i}",
                ts="2026-07-13T10:00:00Z",
            ))

    lines = events_file.read_text().strip().split("\n")
    assert len(lines) == 3

from rcode.core.bus.events import EventPushEnvelope


def test_event_push_envelope_roundtrip():
    envelope = EventPushEnvelope(event={"type": "test", "data": "hello"})
    data = envelope.model_dump()
    assert data["kind"] == "event"
    assert data["event"] == {"type": "test", "data": "hello"}

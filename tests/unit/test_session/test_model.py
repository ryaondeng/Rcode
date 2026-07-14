from rcode.core.session.model import Session


def test_session_serialization():
    session = Session(
        id="sess-123",
        mode="chat",
        title="Test Session",
        created_at="2026-07-14T10:00:00Z",
        updated_at="2026-07-14T10:00:00Z",
    )
    data = session.to_dict()
    assert data["id"] == "sess-123"
    assert data["mode"] == "chat"
    assert data["title"] == "Test Session"
    assert data["status"] == "active"


def test_session_from_dict():
    data = {
        "id": "sess-456",
        "mode": "one_shot",
        "status": "closed",
        "title": "Test",
        "created_at": "2026-07-14T10:00:00Z",
        "updated_at": "2026-07-14T10:00:00Z",
        "run_ids": ["run_1"],
    }
    session = Session.from_dict(data)
    assert session.id == "sess-456"
    assert session.mode == "one_shot"
    assert session.status == "closed"
    assert session.run_ids == ["run_1"]

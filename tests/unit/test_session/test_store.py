import pytest

from rcode.core.session.model import Session
from rcode.core.session.store import SessionStore


def test_write_and_read_meta(tmp_path):
    store = SessionStore(tmp_path)
    session = Session(
        id="sess-123",
        mode="chat",
        title="Test",
        created_at="2026-07-14T10:00:00Z",
        updated_at="2026-07-14T10:00:00Z",
    )
    store.write_meta(session)
    loaded = store.read_meta("sess-123")
    assert loaded is not None
    assert loaded.id == "sess-123"
    assert loaded.mode == "chat"


def test_read_meta_not_found(tmp_path):
    store = SessionStore(tmp_path)
    loaded = store.read_meta("nonexistent")
    assert loaded is None


def test_append_and_read_messages(tmp_path):
    store = SessionStore(tmp_path)
    store.append_message("sess-123", {"role": "user", "content": "hello"})
    store.append_message("sess-123", {"role": "assistant", "content": "hi"})
    messages = store.read_messages("sess-123")
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_append_and_read_notes(tmp_path):
    store = SessionStore(tmp_path)
    store.append_note("sess-123", "Important note")
    notes = store.read_notes("sess-123")
    assert "Important note" in notes

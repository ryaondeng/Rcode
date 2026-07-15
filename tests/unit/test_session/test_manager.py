import pytest

from rcode.core.session.manager import SessionManager
from rcode.core.session.store import SessionStore


@pytest.mark.asyncio
async def test_create_session(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create(mode="chat", title="Test")
    assert session.id.startswith("sess-")
    assert session.mode == "chat"
    assert session.title == "Test"
    assert session.status == "active"


@pytest.mark.asyncio
async def test_send_message(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create()
    run_id = await manager.send_message(session.id, "hello")
    assert run_id.startswith("run_")
    assert session.status == "active"


@pytest.mark.asyncio
async def test_send_message_not_found(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    with pytest.raises(ValueError, match="Session not found"):
        await manager.send_message("nonexistent", "hello")


@pytest.mark.asyncio
async def test_send_message_closed(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create()
    await manager.close(session.id)
    with pytest.raises(ValueError, match="Session is closed"):
        await manager.send_message(session.id, "hello")


@pytest.mark.asyncio
async def test_get_history(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create()
    await manager.send_message(session.id, "hello")
    history = await manager.get_history(session.id)
    assert len(history) == 1
    assert history[0]["role"] == "user"


@pytest.mark.asyncio
async def test_close_session(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create()
    await manager.close(session.id)
    assert session.status == "closed"


@pytest.mark.asyncio
async def test_load_session(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create(mode="chat", title="Test Load")
    loaded = await manager.load(session.id)
    assert loaded is not None
    assert loaded.id == session.id
    assert loaded.title == "Test Load"


@pytest.mark.asyncio
async def test_load_session_not_found(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    loaded = await manager.load("nonexistent")
    assert loaded is None


@pytest.mark.asyncio
async def test_load_context(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create(goal="test goal")
    await manager.send_message(session.id, "hello")
    context = await manager.load_context(session.id)
    assert context is not None
    assert context.goal == "hello"
    assert len(context.messages) == 1


@pytest.mark.asyncio
async def test_load_context_not_found(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    context = await manager.load_context("nonexistent")
    assert context is None


@pytest.mark.asyncio
async def test_save_messages(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create()
    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]
    await manager.save(session.id, messages)
    history = await manager.get_history(session.id)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


@pytest.mark.asyncio
async def test_create_session_with_id(tmp_path):
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session = await manager.create(session_id="custom-id", goal="test")
    assert session.id == "custom-id"
    loaded = await manager.load("custom-id")
    assert loaded is not None

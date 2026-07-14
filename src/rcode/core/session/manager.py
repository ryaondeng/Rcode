from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from rcode.core.session.model import Session, SessionMode
from rcode.core.session.store import SessionStore


class SessionManager:
    """会话业务管理。"""

    def __init__(self, store: SessionStore) -> None:
        self._store = store
        self._sessions: dict[str, Session] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    def _get_lock(self, session_id: str) -> asyncio.Lock:
        if session_id not in self._locks:
            self._locks[session_id] = asyncio.Lock()
        return self._locks[session_id]

    async def create(self, mode: SessionMode = "chat", title: str = "") -> Session:
        """创建新会话。"""
        session_id = f"sess-{uuid.uuid4().hex[:12]}"
        now = datetime.now(UTC).isoformat()
        session = Session(
            id=session_id,
            mode=mode,
            title=title or "New Session",
            created_at=now,
            updated_at=now,
        )
        self._sessions[session_id] = session
        self._store.write_meta(session)
        return session

    async def send_message(self, session_id: str, content: str) -> str:
        """发送消息并返回 run_id。"""
        async with self._get_lock(session_id):
            session = self._sessions.get(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")
            if session.status == "closed":
                raise ValueError("Session is closed")

            # 追加用户消息
            self._store.append_message(session_id, {
                "role": "user",
                "content": content,
                "ts": datetime.now(UTC).isoformat(),
            })

            # 更新状态
            session.status = "active"
            session.updated_at = datetime.now(UTC).isoformat()
            self._store.write_meta(session)

            return f"run_{uuid.uuid4().hex[:8]}"

    async def get_history(self, session_id: str) -> list[dict]:
        """获取会话历史。"""
        return self._store.read_messages(session_id)

    async def get_notes(self, session_id: str) -> str:
        """获取会话笔记。"""
        return self._store.read_notes(session_id)

    async def close(self, session_id: str) -> None:
        """关闭会话。"""
        async with self._get_lock(session_id):
            session = self._sessions.get(session_id)
            if session:
                session.status = "closed"
                session.updated_at = datetime.now(UTC).isoformat()
                self._store.write_meta(session)

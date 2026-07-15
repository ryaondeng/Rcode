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

    async def create(self, session_id: str | None = None, mode: SessionMode = "chat", title: str = "", goal: str = "") -> Session:
        """创建新会话。"""
        if session_id is None:
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

    async def load(self, session_id: str) -> Session | None:
        """加载会话。"""
        # 先从内存缓存找
        if session_id in self._sessions:
            return self._sessions[session_id]
        # 从存储加载
        session = self._store.read_meta(session_id)
        if session:
            self._sessions[session_id] = session
        return session

    async def load_context(self, session_id: str):
        """从已有 session 构建 ExecutionContext。"""
        from rcode.core.context import ExecutionContext

        session = await self.load(session_id)
        if session is None:
            return None

        # 加载历史消息
        messages = self._store.read_messages(session_id)

        # 构建 ExecutionContext
        context = ExecutionContext(
            goal=messages[-1]["content"] if messages else "",
            run_id=f"run_{uuid.uuid4().hex[:8]}",
        )
        context.messages = messages
        return context

    async def save(self, session_id: str, messages: list[dict]) -> None:
        """保存消息到 session。"""
        async with self._get_lock(session_id):
            session = self._sessions.get(session_id)
            if session:
                session.updated_at = datetime.now(UTC).isoformat()
                self._store.write_meta(session)

            # 追加消息
            for msg in messages:
                self._store.append_message(session_id, msg)

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

from __future__ import annotations

import json
from pathlib import Path

from rcode.core.session.model import Session


class SessionStore:
    """会话文件存储。"""

    def __init__(self, root: Path) -> None:
        self._root = root

    def write_meta(self, session: Session) -> None:
        """写入 session 元数据。"""
        path = self._root / session.id / "meta.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(session.to_dict(), ensure_ascii=False, indent=2))

    def read_meta(self, session_id: str) -> Session | None:
        """读取 session 元数据。"""
        path = self._root / session_id / "meta.json"
        if not path.exists():
            return None
        return Session.from_dict(json.loads(path.read_text()))

    def append_message(self, session_id: str, message: dict) -> None:
        """追加消息到 thread.jsonl。"""
        path = self._root / session_id / "thread.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")

    def read_messages(self, session_id: str) -> list[dict]:
        """读取完整 thread。"""
        path = self._root / session_id / "thread.jsonl"
        if not path.exists():
            return []
        messages = []
        for line in path.read_text().splitlines():
            if line.strip():
                messages.append(json.loads(line))
        return messages

    def append_note(self, session_id: str, note: str) -> None:
        """追加笔记到 notes.md。"""
        path = self._root / session_id / "notes.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n{note}\n")

    def read_notes(self, session_id: str) -> str:
        """读取笔记。"""
        path = self._root / session_id / "notes.md"
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

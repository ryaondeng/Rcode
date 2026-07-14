from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


SessionMode = Literal["one_shot", "chat"]
SessionStatus = Literal["active", "waiting_for_input", "closed"]


@dataclass
class Session:
    """会话数据结构。"""

    id: str
    mode: SessionMode
    status: SessionStatus = "active"
    title: str = ""
    created_at: str = ""
    updated_at: str = ""
    run_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "mode": self.mode,
            "status": self.status,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "run_ids": self.run_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Session:
        return cls(**data)

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class JsonRpcSuccess(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Any


class JsonRpcErrorObject(BaseModel):
    code: int
    message: str
    data: Any = None


class JsonRpcError(BaseModel):
    jsonrpc: str = "2.0"
    id: str | None = None
    error: JsonRpcErrorObject


PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class HandlerError(Exception):
    def __init__(self, code: int, message: str, data: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


def make_error(
    id: str | None, code: int, message: str, data: Any = None
) -> JsonRpcError:
    return JsonRpcError(
        id=id,
        error=JsonRpcErrorObject(code=code, message=message, data=data),
    )

from rcode.core.bus.envelope import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    PARSE_ERROR,
    HandlerError,
    JsonRpcError,
    JsonRpcErrorObject,
    JsonRpcRequest,
    JsonRpcSuccess,
    make_error,
)


def test_request_roundtrip():
    req = JsonRpcRequest(id="1", method="core.ping", params={"client": "test"})
    data = req.model_dump()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert data["method"] == "core.ping"
    assert data["params"] == {"client": "test"}


def test_request_default_params():
    req = JsonRpcRequest(id="1", method="core.ping")
    assert req.params == {}


def test_success_roundtrip():
    resp = JsonRpcSuccess(id="1", result={"pong": True})
    data = resp.model_dump()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == "1"
    assert data["result"] == {"pong": True}


def test_error_roundtrip():
    err = JsonRpcError(
        id="1",
        error=JsonRpcErrorObject(code=INTERNAL_ERROR, message="fail"),
    )
    data = err.model_dump()
    assert data["error"]["code"] == INTERNAL_ERROR
    assert data["error"]["message"] == "fail"
    assert data["error"]["data"] is None


def test_error_with_data():
    err = JsonRpcError(
        id="1",
        error=JsonRpcErrorObject(code=INVALID_PARAMS, message="bad", data={"field": "x"}),
    )
    assert err.error.data == {"field": "x"}


def test_error_no_id():
    err = JsonRpcError(error=JsonRpcErrorObject(code=PARSE_ERROR, message="parse"))
    assert err.id is None


def test_make_error():
    err = make_error("1", METHOD_NOT_FOUND, "not found")
    assert err.id == "1"
    assert err.error.code == METHOD_NOT_FOUND
    assert err.error.message == "not found"
    assert err.error.data is None


def test_make_error_with_data():
    err = make_error("1", INVALID_REQUEST, "bad", {"extra": "info"})
    assert err.error.data == {"extra": "info"}


def test_handler_error():
    e = HandlerError(INTERNAL_ERROR, "something broke", {"debug": 1})
    assert e.code == INTERNAL_ERROR
    assert str(e) == "something broke"
    assert e.data == {"debug": 1}


def test_error_codes():
    assert PARSE_ERROR == -32700
    assert INVALID_REQUEST == -32600
    assert METHOD_NOT_FOUND == -32601
    assert INVALID_PARAMS == -32602
    assert INTERNAL_ERROR == -32603

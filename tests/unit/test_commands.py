from rcode.core.bus.commands import PingCommand, PongResult


def test_ping_command_roundtrip():
    cmd = PingCommand(client="cli")
    data = cmd.model_dump()
    assert data["type"] == "core.ping"
    assert data["client"] == "cli"


def test_pong_result_roundtrip():
    result = PongResult(
        server_version="0.1.0",
        uptime_ms=1234,
        received_at="2026-07-12T10:00:00Z",
    )
    data = result.model_dump()
    assert data["server_version"] == "0.1.0"
    assert data["uptime_ms"] == 1234
    assert data["received_at"] == "2026-07-12T10:00:00Z"

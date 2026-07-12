from rcode.core.config import RcodeConfig, get_config


def test_default_config():
    config = RcodeConfig()
    assert config.host == "127.0.0.1"
    assert config.port == 7437
    assert config.logging.level == "INFO"
    assert "~/.rcode/logs/core.log" in config.logging.file


def test_get_config_defaults(monkeypatch):
    monkeypatch.delenv("RCODE_HOST", raising=False)
    monkeypatch.delenv("RCODE_PORT", raising=False)
    monkeypatch.delenv("RCODE_LOG_LEVEL", raising=False)
    monkeypatch.delenv("RCODE_LOG_FILE", raising=False)
    monkeypatch.delenv("RCODE_CONFIG", raising=False)
    config = get_config()
    assert config.host == "127.0.0.1"
    assert config.port == 7437


def test_get_config_from_env(monkeypatch):
    monkeypatch.setenv("RCODE_HOST", "0.0.0.0")
    monkeypatch.setenv("RCODE_PORT", "9999")
    monkeypatch.setenv("RCODE_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("RCODE_LOG_FILE", "/tmp/test.log")
    monkeypatch.delenv("RCODE_CONFIG", raising=False)
    config = get_config()
    assert config.host == "0.0.0.0"
    assert config.port == 9999
    assert config.logging.level == "DEBUG"
    assert config.logging.file == "/tmp/test.log"

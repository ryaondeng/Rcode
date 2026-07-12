import os

from rcode.core.config import RcodeConfig, load_config


def test_default_config():
    config = RcodeConfig()
    assert config.host == "127.0.0.1"
    assert config.port == 7437
    assert config.log_level == "INFO"
    assert config.log_file is None


def test_load_config_defaults(monkeypatch):
    monkeypatch.delenv("RCODE_HOST", raising=False)
    monkeypatch.delenv("RCODE_PORT", raising=False)
    monkeypatch.delenv("RCODE_LOG_LEVEL", raising=False)
    monkeypatch.delenv("RCODE_LOG_FILE", raising=False)
    config = load_config()
    assert config.host == "127.0.0.1"
    assert config.port == 7437


def test_load_config_from_env(monkeypatch):
    monkeypatch.setenv("RCODE_HOST", "0.0.0.0")
    monkeypatch.setenv("RCODE_PORT", "9999")
    monkeypatch.setenv("RCODE_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("RCODE_LOG_FILE", "/tmp/test.log")
    config = load_config()
    assert config.host == "0.0.0.0"
    assert config.port == 9999
    assert config.log_level == "DEBUG"
    assert config.log_file == "/tmp/test.log"

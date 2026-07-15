from rcode.core.config import RcodeConfig, get_config, LLMConfig, SessionConfig, CompactConfig


def test_default_config():
    config = RcodeConfig()
    assert config.host == "127.0.0.1"
    assert config.port == 7437
    assert config.logging.level == "INFO"
    assert "~/.rcode/logs/core.log" in config.logging.file
    assert config.llm.model == "mimo-v2.5"
    assert config.compact.threshold == 0.0


def test_llm_config():
    config = LLMConfig()
    assert config.model == "mimo-v2.5"
    assert config.timeout == 120
    assert config.max_retries == 2


def test_session_config():
    config = SessionConfig()
    assert config.dir == ".rcode/sessions"
    assert config.auto_archive_days == 30


def test_compact_config():
    config = CompactConfig()
    assert config.threshold == 0.0
    assert config.tool_result_limit == 8000
    assert config.tool_result_keep == 4000


def test_config_forbid_extra():
    """测试未知字段被拒绝"""
    try:
        RcodeConfig(unknown_field="value")
        assert False, "Should have raised error"
    except Exception as e:
        assert "extra" in str(e).lower() or "forbidden" in str(e).lower()


def test_get_config_defaults(monkeypatch):
    monkeypatch.delenv("RCODE_HOST", raising=False)
    monkeypatch.delenv("RCODE_PORT", raising=False)
    monkeypatch.delenv("RCODE_LOG_LEVEL", raising=False)
    monkeypatch.delenv("RCODE_LLM_MODEL", raising=False)
    config = get_config()
    assert config.host == "127.0.0.1"
    assert config.port == 7437


def test_get_config_from_env(monkeypatch):
    monkeypatch.setenv("RCODE_HOST", "0.0.0.0")
    monkeypatch.setenv("RCODE_PORT", "9999")
    monkeypatch.setenv("RCODE_LLM_MODEL", "custom-model")
    monkeypatch.delenv("RCODE_CONFIG", raising=False)
    config = get_config()
    assert config.host == "0.0.0.0"
    assert config.port == 9999
    assert config.llm.model == "custom-model"

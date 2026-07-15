import pytest
import tempfile
from pathlib import Path

from rcode.core.config import RcodeConfig, load_config, LLMConfig, CompactConfig


# 功能：测试配置加载集成
# 设计：验证配置能正确加载
def test_config_load():
    config = load_config()
    assert isinstance(config, RcodeConfig)
    assert config.llm.model == "mimo-v2.5"
    assert config.compact.threshold == 0.0


# 功能：测试配置校验
# 设计：验证未知字段被拒绝
def test_config_validation():
    try:
        RcodeConfig(unknown_field="value")
        assert False, "Should have raised error"
    except Exception as e:
        assert "extra" in str(e).lower() or "forbidden" in str(e).lower()


# 功能：测试环境变量覆盖
# 设计：验证环境变量能覆盖默认值
def test_config_env_override(monkeypatch):
    monkeypatch.setenv("RCODE_LLM_MODEL", "custom-model")
    config = load_config()
    assert config.llm.model == "custom-model"

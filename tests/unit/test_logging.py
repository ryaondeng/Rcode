import logging
from unittest.mock import patch

from rcode.core.config import LoggingConfig, RcodeConfig
from rcode.core.logging_setup import setup_logging


def test_setup_logging_default():
    config = RcodeConfig()
    with patch("logging.basicConfig") as mock_basic:
        setup_logging(config)
        mock_basic.assert_called_once()
        call_kwargs = mock_basic.call_args
        assert call_kwargs[1]["level"] == logging.INFO


def test_setup_logging_debug():
    config = RcodeConfig(logging=LoggingConfig(level="DEBUG"))
    with patch("logging.basicConfig") as mock_basic:
        setup_logging(config)
        call_kwargs = mock_basic.call_args
        assert call_kwargs[1]["level"] == logging.DEBUG

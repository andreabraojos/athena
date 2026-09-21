import logging
import unittest
from unittest.mock import patch

from src.main import configure_logging


class TestLoggingConfiguration(unittest.TestCase):

    @patch("src.main.logging.basicConfig")
    @patch("src.main.LOG_PATH")
    def test_configures_file_logging(
        self,
        mock_log_path,
        mock_basic_config
    ) -> None:
        configure_logging()

        mock_log_path.parent.mkdir.assert_called_once_with(
            parents=True,
            exist_ok=True
        )

        mock_basic_config.assert_called_once_with(
            filename=mock_log_path,
            level=logging.INFO,
            format=(
                "%(asctime)s %(levelname)s "
                "%(name)s %(message)s"
            ),
            encoding="utf-8"
        )
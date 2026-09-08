import os
import unittest
from unittest.mock import patch

from src.config import load_llm_config


class TestLLMConfig(unittest.TestCase):

    @patch.dict(os.environ, {}, clear=True)
    def test_loads_default_values(self) -> None:
        config = load_llm_config()

        self.assertEqual(
            config.url,
            "http://localhost:11434/api/generate"
        )
        self.assertEqual(config.model, "qwen3:8b")
        self.assertEqual(config.timeout, 120.0)


    @patch.dict(
        os.environ,
        {
            "ATHENA_OLLAMA_URL": "http://ollama-test:11434/api/generate",
            "ATHENA_OLLAMA_MODEL": "modelo-test",
            "ATHENA_OLLAMA_TIMEOUT": "30.5"
        },
        clear=True
    )
    def test_loads_values_from_environment(self) -> None:
        config = load_llm_config()

        self.assertEqual(
            config.url,
            "http://ollama-test:11434/api/generate"
        )
        self.assertEqual(config.model, "modelo-test")
        self.assertEqual(config.timeout, 30.5)


    @patch.dict(
        os.environ,
        {"ATHENA_OLLAMA_TIMEOUT": "mucho"},
        clear=True
    )
    def test_rejects_a_non_numeric_timeout(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "ATHENA_OLLAMA_TIMEOUT debe ser un número"
        ):
            load_llm_config()
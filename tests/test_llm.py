import unittest

from src.config import LLMConfig
from src.llm import LLM


class TestLLM(unittest.TestCase):

    def test_uses_provided_configuration(self) -> None:
        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        self.assertEqual(
            llm.url,
            "http://servidor-prueba/api/generate"
        )
        self.assertEqual(llm.model, "modelo-prueba")
        self.assertEqual(llm.timeout, 30.0)
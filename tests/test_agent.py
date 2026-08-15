import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.agent import Athena


class FakeLLM:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "Respuesta simulada"


class TestAthenaMemoryIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.memory_path = Path(self.temp_directory.name) / "memory.json"
        self.llm = FakeLLM()

        self.athena = Athena(
            llm=self.llm,
            memory_path=self.memory_path
        )

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_build_prompt_includes_persistent_memory(self) -> None:
        self.athena.memory.save("nombre", "Andrea")

        prompt = self.athena.build_prompt("¿Cómo me llamo?")

        self.assertIn('"nombre": "Andrea"', prompt)
        self.assertIn("¿Cómo me llamo?", prompt)

    @patch("builtins.print")
    @patch("builtins.input", return_value="Hola")
    def test_chat_sends_prompt_with_memory_to_llm(self, mock_input, mock_print) -> None:
        self.athena.memory.save("nombre", "Andrea")

        self.athena.chat()

        self.assertEqual(len(self.llm.prompts), 1)
        self.assertIn('"nombre": "Andrea"', self.llm.prompts[0])
        self.assertIn("Pregunta del usuario:\nHola", self.llm.prompts[0])
        mock_print.assert_called_once_with("\nAthena: ", "Respuesta simulada")

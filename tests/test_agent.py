import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from src.agent import Athena
from src.llm import LLMError


class FakeLLM:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "Respuesta simulada"


class FailingLLM:
    def generate(self, prompt: str) -> str:
        raise LLMError(
            "No se pudo conectar con Ollama."
        )


class TestAthenaMemoryIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.memory_path = Path(self.temp_directory.name) / "memory.json"
        self.llm = FakeLLM()
        self.tasks_path = (
            Path(self.temp_directory.name) / "tasks.json"
        )

        self.athena = Athena(
            llm=self.llm,
            memory_path=self.memory_path,
            tasks_path=self.tasks_path

        )

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_build_prompt_includes_persistent_memory(self) -> None:
        self.athena.memory.save("nombre", "Andrea")

        prompt = self.athena.build_prompt("¿Cómo me llamo?")

        self.assertIn('"nombre": "Andrea"', prompt)
        self.assertIn("¿Cómo me llamo?", prompt)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Hola", "salir"])
    def test_chat_sends_prompt_with_memory_to_llm(
        self,
        mock_input, 
        mock_print
    ) -> None:
        self.athena.memory.save("nombre", "Andrea")

        self.athena.chat()

        self.assertEqual(len(self.llm.prompts), 1)
        self.assertIn('"nombre": "Andrea"', self.llm.prompts[0])
        self.assertIn("Pregunta del usuario:\nHola", self.llm.prompts[0])
        mock_print.assert_any_call("\nAthena: ", "Respuesta simulada")
        mock_print.assert_any_call("Athena: Hasta pronto.")

    def test_remember_saves_a_new_value(self) -> None:
        self.athena.remember("ciudad = Madrid")

        self.assertEqual(
            self.athena.memory.get("ciudad"),
            "Madrid"
        )

    def test_remember_updates_an_existing_value(self) -> None:
        self.athena.memory.save("ciudad", "Madrid")

        self.athena.remember("ciudad = Valencia")

        self.assertEqual(
            self.athena.memory.get("ciudad"),
            "Valencia"
        )

    def test_forget_deletes_an_existing_value(self) -> None:
        self.athena.memory.save("ciudad", "Madrid")

        self.athena.forget("ciudad")

        self.assertIsNone(
            self.athena.memory.get("ciudad")
        )

    def test_athena_starts_with_an_empty_task_manager(self) -> None:
        self.assertEqual(self.athena.tasks.list_all(), [])

    @patch("builtins.print")
    @patch(
        "builtins.input",
        side_effect=["tarea añade Estudiar inglés", "salir"]
    )

    def test_chat_adds_a_task(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        self.assertEqual(
            self.athena.tasks.list_all(),
            [
                {
                    "id":1,
                    "title": "Estudiar inglés",
                    "completed": False,
                    "due_date": None
                }
            ]
        )

    @patch("builtins.print")
    @patch(
        "builtins.input",
        side_effect=["tareas", "salir"]
    )
    def test_chat_shows_tasks_with_due_date(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.tasks.add(
            "Entregar proyecto inglés",
            due_date= "2026-08-25")

        self.athena.chat()

        mock_print.assert_any_call(
             "- [ ] 1: Entregar proyecto inglés | fecha: 2026-08-25")
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["tarea completa 1", "salir"])
    def test_chat_completes_a_task(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.tasks.add("Estudiar francés", due_date="2026-08-26")

        self.athena.chat()

        tasks = self.athena.tasks.list_all()

        self.assertTrue(tasks[0]["completed"])

        mock_print.assert_any_call(
            "Athena: He completado la tarea 1."
        )
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["tarea elimina 1", "salir"])
    def test_chat_deletes_a_task(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.tasks.add("Estudiar francés", due_date="2026-08-26")

        self.athena.chat()

        self.assertEqual(self.athena.tasks.list_all(), [])

        mock_print.assert_any_call(
            "Athena: He eliminado la tarea 1."
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["pendientes", "salir"])
    def test_chat_shows_only_pending_tasks(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.tasks.add("Estudiar inglés")
        self.athena.tasks.add("Estudiar francés")

        self.athena.tasks.complete(2)

        self.athena.chat()

        mock_print.assert_any_call(
            "- [ ] 1: Estudiar inglés"
        )

        self.assertNotIn(
            call("- [✓] 2: Estudiar francés"),
            mock_print.call_args_list
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["hoy", "salir"])
    @patch("src.agent.date")
    def test_chat_shows_only_pending_tasks_due_today(
        self,
        mock_date,
        mock_input,
        mock_print
    ) -> None:
        mock_date.today.return_value.isoformat.return_value = (
            "2026-09-04"
        )

        self.athena.tasks.add(
            "Tarea de hoy",
            due_date="2026-09-04"
        )

        self.athena.tasks.add(
            "Tarea de mañana",
            due_date="2026-09-05"
        )

        self.athena.tasks.add(
            "Tarea completada",
            due_date="2026-09-04"
        )
        self.athena.tasks.complete(3)

        self.athena.chat()

        mock_print.assert_any_call(
            "- [ ] 1: Tarea de hoy | fecha: 2026-09-04"
        )

        self.assertNotIn(
            call(
                "- [ ] 2: Tarea de mañana | fecha: 2026-09-05"
            ),
            mock_print.call_args_list
        )

        self.assertNotIn(
            call(
                "- [✓] 3: Tarea completada | fecha: 2026-09-04"
            ),
            mock_print.call_args_list
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["tarea añade Entregar proyecto | 2026-09-10",
                                          "salir"])
    def test_chat_adds_a_task_with_due_date(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        self.assertEqual(
            self.athena.tasks.list_all(),
            [            
                {
                    "id":1,
                    "title": "Entregar proyecto",
                    "completed": False,
                    "due_date": "2026-09-10"
                }
            ]
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["tarea completa 999", "salir"])
    def test_chat_handles_unknown_task_id(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: No existe una tarea con ID 999."
        )

        mock_print.assert_any_call(
            "Athena: Hasta pronto."
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["tarea añade Entregar proyecto | 10-09-2026", "salir"])
    def test_chat_handles_invalid_task_date(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: "
            "tarea añade título | YYYY-MM-DD"
        )

        self.assertEqual(
            self.athena.tasks.list_all(), []
        )

        mock_print.assert_any_call(
            "Athena: Hasta pronto."
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Hola", "salir"])
    def test_chat_continues_after_llm_error(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena = Athena(
            llm=FailingLLM(),
            memory_path=self.memory_path,
            tasks_path=self.tasks_path
        )

        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: No se pudo conectar con Ollama."
        )
        mock_print.assert_any_call(
            "Athena: Hasta pronto."
        )

    @patch("builtins.print")
    @patch("builtins.input",
            side_effect=["olvida color", "salir"])
    def test_chat_forgets_a_value(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.memory.save("color", "azul")

        self.athena.chat()

        self.assertIsNone(
            self.athena.memory.get("color")
        )
        self.assertEqual(self.llm.prompts, [])

        mock_print.assert_any_call(
            'Athena: He olvidado "color".'
        )

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["recuerda persona = Laura", "salir"])
    def test_chat_remembers_a_value_preserving_original_case(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        self.assertEqual(
            self.athena.memory.get("persona"),
            "Laura"
        )
        self.assertEqual(self.llm.prompts, [])

        mock_print.assert_any_call(
            'Athena: He guardado "persona".'
        )

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["recuerda", "salir"])
    def test_chat_handles_remember_without_content(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: recuerda clave = valor"
        )

        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["tarea añade", "salir"])
    def test_chat_handles_add_task_without_content(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: "
            "tarea añade título | YYYY-MM-DD"
        )

        self.assertEqual(self.athena.tasks.list_all(), [])
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["tarea completa", "salir"])
    def test_chat_handles_complete_task_without_id(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: tarea completa id"
        )
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["tarea elimina", "salir"])
    def test_chat_handles_delete_task_without_id(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: tarea elimina id"
        )
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["tarea completa abc", "salir"])
    def test_chat_handles_non_numeric_task_id(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: Usa el formato: tarea completa id"
        )
        self.assertEqual(self.llm.prompts, [])

    @patch("builtins.print")
    @patch("builtins.input",
           side_effect=["tarea elimina 999", "salir"])
    def test_chat_handles_unknown_task_id_when_deleting(
        self,
        mock_input,
        mock_print
    ) -> None:
        self.athena.chat()

        mock_print.assert_any_call(
            "Athena: No existe una tarea con ID 999."
        )
        self.assertEqual(self.llm.prompts, [])

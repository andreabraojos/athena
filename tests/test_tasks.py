import tempfile
import unittest
from pathlib import Path

from src.tasks import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()

        self.tasks_path = (
            Path(self.temp_directory.name) / "tasks.json"
        )

        self.tasks = TaskManager(self.tasks_path)


    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_add_creates_a_pending_task(self) -> None:
        self.tasks.add("Estudiar inglés")

        self.assertEqual(
            self.tasks.tasks,
            [
                {
                    "id": 1,
                    "title": "Estudiar inglés",
                    "completed": False,
                    "due_date": None
                }
            ]
        )

    def test_list_all_returns_added_tasks(self) -> None:
        self.tasks.add("Estudiar inglés")

        tasks = self.tasks.list_all()

        self.assertEqual(
            tasks,
            [
                {
                    "id":1,
                    "title": "Estudiar inglés",
                    "completed": False,
                    "due_date": None
                }
            ]
        )

    def test_complete_marks_a_task_as_completed(self) -> None:
        self.tasks.add ("Estudiar inglés")

        self.tasks.complete(1)

        self.assertTrue(self.tasks.tasks[0]["completed"])

    def test_complete_rejects_an_unknown_id(self) -> None:
        with self.assertRaises(KeyError):
            self.tasks.complete(999)

    def test_delete_removes_a_task(self) -> None:
        self.tasks.add("Estudiar inglés")

        self.tasks.delete(1)

        self.assertEqual(self.tasks.tasks, [])

    def test_delete_rejects_an_unknown_id(self) -> None:
        with self.assertRaises(KeyError):
            self.tasks.delete(999)

    def test_complete_persists_the_change_on_disk(self) -> None:
        self.tasks.add("Estudiar inglés")
        self.tasks.complete(1)

        recovered_tasks = TaskManager(self.tasks_path)

        self.assertTrue(recovered_tasks.tasks[0]["completed"])

    def test_add_rejects_an_empty_tittle(self) -> None:
        with self.assertRaises(ValueError):
            self.tasks.add("    ")

    def test_add_persists_a_task_on_disk(self) -> None:
        self.tasks.add("Estudiar inglés")

        recovered_tasks = TaskManager(self.tasks_path)

        self.assertEqual(
            recovered_tasks.tasks[0]["title"],
            "Estudiar inglés"
        )

    def test_delete_persists_the_removal_on_disk(self) -> None:
        self.tasks.add ("Estudiar inglés")

        self.tasks.delete(1)

        recovered_tasks = TaskManager(self.tasks_path)

        self.assertEqual(recovered_tasks.tasks, [])

    def test_add_saves_a_due_date(self) -> None:
        self.tasks.add(
            "Entregar proyecto",
            due_date="2026-08-25"
        )

        self.assertEqual(
            self.tasks.tasks[0]["due_date"],
            "2026-08-25"
        )

    def test_add_rejects_an_invalid_due_date(self) -> None:
        with self.assertRaises(ValueError):
            self.tasks.add(
                "Entregar proyecto",
                due_date="25-08-2026"
            )

    def test_pending_excludes_completed_tasks(self) -> None:
        self.tasks.add("Pendiente")
        self.tasks.add("Completada")
        self.tasks.complete(2)

        self.assertEqual(
            self.tasks.pending()[0]["title"],
            "Pendiente"
        )

    def test_due_on_returns_only_pending_tasks_for_that_date(self) -> None:
        self.tasks.add("Tarea de hoy", due_date="2026-08-24")
        self.tasks.add("Tarea de mañana", due_date="2026-08-25")
        self.tasks.add("Completada", due_date="2026-08-24")
        self.tasks.complete(3)

        tasks = self.tasks.due_on("2026-08-24")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Tarea de hoy")

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
                    "completed": False
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
                    "completed": False
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


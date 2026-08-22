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

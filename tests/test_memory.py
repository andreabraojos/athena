import json 
import tempfile
import unittest
from pathlib import Path

from src.memory import Memory


class TestMemory(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()

        self.memory_path = (
            Path(self.temp_directory.name) / "memory.json"
        )

        self.memory = Memory(self.memory_path)

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_creates_memory_file_if_it_does_not_exist(self) -> None:
        self.assertTrue(self.memory_path.exists())

    def test_new_memory_starts_empty(self) -> None:
        self.assertEqual(self.memory.data, {})

    def test_save_adds_a_new_value(self) -> None:
        self.memory.save("nombre", "Andrea")

        self.assertEqual(
            self.memory.get("nombre"),
            "Andrea"
        )

    def test_save_persists_value_on_disk(self) -> None:
        self.memory.save("nombre", "Andrea")

        with self.memory_path.open(
            mode="r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, {"nombre": "Andrea"})

    def test_load_recovers_values_from_disk(self) -> None:
        self.memory.save("nombre", "Andrea")
        recovered_memory = Memory(self.memory_path)

        self.assertEqual(recovered_memory.get("nombre"), "Andrea")

    def test_save_rejects_an_existing_key(self) -> None:
        self.memory.save("nombre", "Andrea")

        with self.assertRaises(KeyError):
            self.memory.save("nombre", "Otra persona")

    def test_update_changes_an_existing_value(self) -> None:
        self.memory.save("nombre", "Andrea")
        self.memory.update("nombre", "Andrés")

        self.assertEqual(self.memory.get("nombre"), "Andrés")

    def test_delete_removes_an_existing_value(self) -> None:
        self.memory.save("nombre", "Andrea")
        self.memory.delete("nombre")

        self.assertIsNone(self.memory.get("nombre"))
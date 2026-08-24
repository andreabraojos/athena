import json
from pathlib import Path
from typing import Any
from datetime import date


class TaskManager:

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.tasks: list[dict[str, Any]] = []
        self.load()

    def add(
        self,
        title: str,
        due_date: str | None = None
    ) -> None:
        title = title.strip()

        if not title:
            raise ValueError("El título de la tarea no puede estar vacío.")

        if due_date is not None:
            try:
                date.fromisoformat(due_date)
            except ValueError as error:
                raise ValueError(
                    "La fecha debe tener formato YYYY-MM-DD."
                ) from error

        next_id = max(
            (task["id"] for task in self.tasks),
            default=0
        ) + 1

        task = {
            "id": next_id,
            "title": title,
            "completed": False,
            "due_date": due_date
        }

        self.tasks.append(task)
        self.save_to_disk()

    def list_all(self) -> list[dict[str, Any]]:
        return [task.copy() for task in self.tasks]

    def complete(self, task_id: int) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_to_disk()
                return


        raise KeyError(
            f"No se ha encontrado la tarea con ID {task_id}."
            )

    def delete(self, task_id: int) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_to_disk()
                return

        raise KeyError(
            f"No se ha encontrado la tarea con ID {task_id}."
        )

    def pending(self) -> list[dict[str, Any]]:
        return[
            task.copy()
            for task in self.tasks
            if not task["completed"]
        ]

    def due_on(self, due_date: str) -> list[dict[str, Any]]:
        return[
            task.copy()
            for task in self.tasks
            if(
                not task["completed"]
                and task.get("due_date") == due_date
            )
        ]

    def load(self) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():
            self.save_to_disk()
            return

        try:
            with self.file_path.open(
                mode="r",
                encoding="utf-8"
            ) as file:
                loaded_tasks = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"El archivo de tareas no contiene JSON válido: "
                f"{self.file_path}"
            ) from error

        if not isinstance(loaded_tasks, list):
            raise ValueError(
                "El contenido del archivo de tareas debe ser "
                "una lista JSON."
            )

        self.tasks = loaded_tasks

    def save_to_disk(self) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.file_path.open(
            mode="w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.tasks,
                file,
                ensure_ascii=False,
                indent=4
            )
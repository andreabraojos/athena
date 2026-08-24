from pathlib import Path
import json
from datetime import date

try:
    from .llm import LLM
    from .memory import Memory
    from .tasks import TaskManager
except ImportError:
    from llm import LLM
    from memory import Memory
    from tasks import TaskManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Athena:
    """
    Agente principal.

    Coordina todos los componentes del sistema.
    """

    def __init__(
        self,
        llm: LLM | None = None,
        memory_path: Path | None = None, 
        tasks_path: Path | None = None
    ):
        print("Inicializando Athena...")
        self.llm = llm or LLM()

        self.memory = Memory(memory_path or PROJECT_ROOT / "data" / "memory.json")

        self.tasks = TaskManager(
            tasks_path or PROJECT_ROOT / "data" / "tasks.json"
        )

    def build_prompt(self, question: str) -> str:
        """Construye el prompt con el contexto persistente disponible."""

        memory_context = json.dumps(
            self.memory.data,
            ensure_ascii=False,
            indent=2
        )

        return (
            "Eres Athena, un asistente personal útil.\n"
            "Puedes usar la memoria persistente siguiente únicamente cuando sea "
            "relevante para responder. No inventes datos ni afirmes que recuerdas "
            "algo que no aparezca en ella.\n\n"
            f"Memoria persistente:\n{memory_context}\n\n"
            f"Pregunta del usuario:\n{question}"
        )

    def show_memory(self) -> None:
        if not self.memory.data:
            print("Athena: No tengo recuerdos guardados.")
            return

        print("Athena: Esto es lo que recuerdo:")

        for key, value in self.memory.data.items():
            print(f"- {key}: {value}")

    def remember(self, content: str) -> None:
        key, separator, value = content.partition("=")

        key = key.strip().lower()
        value = value.strip()

        if not separator or not key or not value:
            print("Athena: Usa el formato: recuerda clave = valor")
            return

        if key in self.memory.data:
            self.memory.update(key, value)
        else:
            self.memory.save(key, value)

        print(f'Athena: He guardado "{key}".')

    def forget(self, key: str) -> None:
        key = key.strip().lower()

        if not key:
            print("Athena: Usa el formato: olvida clave")
            return

        try:
            self.memory.delete(key)
        except KeyError:
            print(f'Athena: No tengo ningún recuerdo llamado "{key}".')
            return

        print(f'Athena: He olvidado "{key}".')

    def add_task(self, content: str) -> None:
        title, separator, due_date = content.partition("|")

        title = title.strip()
        due_date = due_date.strip() if separator else None

        try:
            self.tasks.add(title, due_date)
        except ValueError:
            print(
                "Athena: Usa el formato: " \
                "tarea añade título | YYYY-MM-DD"
            )
            return

        print(f'Athena: He añadido la tarea "{title}".')

    def show_tasks(self) -> None:
        tasks = self.tasks.list_all()

        if not tasks:
            print("Athena: No tienes tareas guardadas.")
            return

        print("Athena: Estas son tus tareas:")

        for task in tasks:
            status = "✓" if task["completed"] else " "
            print(f'- [{status}] {task["id"]}: {task["title"]}')

    def complete_task(self, task_id_text: str) -> None:
        try:
            task_id = int(task_id_text)
            self.tasks.complete(task_id)
        except ValueError:
            print("Athena: Usa el formato: tarea completa id")
            return
        except KeyError:
            print(f'Athena: No existe una tarea con ID {task_id_text}.')
            return

        print(f"Athena: He completado la tarea {task_id}.")

    def delete_task(self, task_id_text: str) -> None:
        try:
            task_id = int(task_id_text)
            self.tasks.delete(task_id)
        except ValueError:
            print("Athena: Usa el formato: tarea eliminada id")
            return
        except KeyError:
            print(f'Athena: No existe una tarea con ID {task_id_text}.')
            return

        print(f"Athena: He eliminado la tarea {task_id}.")

    def show_pending_tasks(self) -> None:
        tasks = self.tasks.pending()

        if not tasks:
            print("Athena: No tienes tareas pendientes.")
            return

        print("Athena: Estas son tus tareas pendientes:")

        for task in tasks:
            print(f'- [{task["id"]}] {task["title"]}')

    def show_today_tasks(self) -> None:
        today = date.today().isoformat()
        tasks = self.tasks.due_on(today)

        if not tasks:
            print("Athena: No tienes tareas pendientes para hoy.")
            return

        print("Athena: Estas son tus tareas para hoy:")

        for task in tasks:
            print(f'- [{task["id"]}] {task["title"]}')    
            
    def chat(self):

        try:

            while True:
                pregunta = input("Tú: ")

                comando = pregunta.strip().lower()

                if comando == "memoria":
                    self.show_memory()
                    continue

                if comando.startswith("recuerda "):
                    content = pregunta.strip()[len("recuerda "):]
                    self.remember(content)
                    continue

                if comando == "olvida" or comando.startswith("olvida "):
                    key = pregunta.strip()[len("olvida"):].strip()
                    self.forget(key)
                    continue

                if comando == "tarea añade" or comando.startswith("tarea añade"):
                    content = pregunta.strip()[len("tarea añade"):].strip()
                    self.add_task(content)
                    continue

                if comando == "tareas":
                    self.show_tasks()
                    continue

                if comando == "tarea completa" or comando.startswith("tarea completa "):
                    task_id_text = pregunta.strip()[len("tarea completa"):].strip()
                    self.complete_task(task_id_text)
                    continue

                if comando == "tarea elimina" or comando.startswith("tarea elimina "):
                    task_id_text = pregunta.strip()[len("tarea elimina"):].strip()
                    self.delete_task(task_id_text)
                    continue

                if comando == "pendientes":
                    self.show_pending_tasks()
                    continue

                if comando == "hoy":
                    self.show_today_tasks()
                    continue


                if comando == "salir":
                    print("Athena: Hasta pronto.")
                    break

                respuesta = self.llm.generate(self.build_prompt(pregunta))

                print("\nAthena: ", respuesta)

        except KeyboardInterrupt:
            print("\nAthena: Hasta pronto.")




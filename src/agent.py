from pathlib import Path
import json

try:
    from .llm import LLM
    from .memory import Memory
except ImportError:
    from llm import LLM
    from memory import Memory

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Athena:
    """
    Agente principal.

    Coordina todos los componentes del sistema.
    """

    def __init__(self, llm: LLM | None = None, memory_path: Path | None = None):
        print("Inicializando Athena...")
        self.llm = llm or LLM()

        self.memory = Memory(memory_path or PROJECT_ROOT / "data" / "memory.json")

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
    def chat(self):

        try:

            while True:
                pregunta = input("Tú: ")

                comando = pregunta.strip().lower()

                if comando == "salir":
                    print("Athena: Hasta pronto.")
                    break

                respuesta = self.llm.generate(self.build_prompt(pregunta))

                print("\nAthena: ", respuesta)

        except KeyboardInterrupt:
            print("\nAthena: Hasta pronto.")

import json
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.agent import Athena
from src.llm import LLMError

CASES_PATH = Path(__file__).with_name("cases.json")


class EvaluationLLM:
    def __init__(
        self,
        error_message: str | None = None
    ) -> None:
        self.prompts: list[str] = []
        self.error_message = error_message

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if self.error_message is not None:
            raise LLMError(self.error_message)
        return "Respuesta simulada"


def load_cases() -> list[dict]:
    with CASES_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def run_case(case: dict) -> tuple[str, int]:
    with tempfile.TemporaryDirectory() as temp_directory:
        temp_path = Path(temp_directory)
        llm = EvaluationLLM(
            error_message=case.get("llm_error")
        )
        output = StringIO()
        inputs = [*case["inputs"], "salir"]

        with patch("src.agent.date") as mock_date:
            mock_date.today.return_value.isoformat.return_value = (
                "2030-01-15"
            )

            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(output):
                    athena = Athena(
                        llm=llm,
                        memory_path=temp_path / "memory.json",
                        tasks_path=temp_path / "tasks.json"
                    )
                    athena.chat()

        return output.getvalue(), len(llm.prompts)


def evaluate_case(case: dict) -> dict:
    output, llm_calls = run_case(case)

    missing_output = [
        expected
        for expected in case["expected_output"]
        if expected not in output
    ]

    errors = []

    if missing_output:
        errors.append(
            f"Faltan fragmentos: {missing_output}"
        )

    if llm_calls != case["expected_llm_calls"]:
        errors.append(
            "Llamadas al LLM: "
            f"esperadas={case['expected_llm_calls']} "
            f"reales={llm_calls}"
        )

    return {
        "name": case["name"],
        "category": case["category"],
        "passed": not errors,
        "errors": errors
    }


def main() -> None:
    cases = load_cases()
    results = [
        evaluate_case(case)
        for case in cases
    ]

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"[{status}] "
            f"{result['category']}/{result['name']}"
        )

        for error in result["errors"]:
            print(f" - {error}")

    passed = sum(
        1 for result in results
        if result["passed"]
    )
    total = len(results)
    rate = (passed / total * 100) if total else 0.0

    categories = {}

    for result in results:
        category = result["category"]

        if category not in categories:
            categories[category] = {
                "passed": 0,
                "total": 0
            }

        categories[category]["total"] += 1

        if result["passed"]:
            categories[category]["passed"] += 1

    print()
    print("Resultados por categoría:")

    for category in sorted(categories):
        category_passed = categories[category]["passed"]
        category_total = categories[category]["total"]
        category_rate = (
            category_passed / category_total * 100
        )

        print(
            f"- {category}: "
            f"{category_passed}/{category_total} "
            f"({category_rate:.1f}%)"
        )
    print(f"Resultado global: {passed}/{total} ({rate:.1f}%)")

    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
import os
from dataclasses import dataclass



@dataclass(frozen=True)
class LLMConfig:
    url: str
    model: str
    timeout: float


def load_llm_config() -> LLMConfig:
    url = os.getenv(
        "ATHENA_OLLAMA_URL",
        "http://localhost:11434/api/generate"
    )

    model = os.getenv(
        "ATHENA_OLLAMA_MODEL",
        "qwen3:8b"
    )

    timeout_text = os.getenv(
        "ATHENA_OLLAMA_TIMEOUT",
        "120"
    )

    try:
        timeout = float(timeout_text)
    except ValueError as error:
        raise ValueError(
            "ATHENA_OLLAMA_TIMEOUT debe ser un número"
        ) from error

    if timeout <= 0:
        raise ValueError(
            "ATHENA_OLLAMA_TIMEOUT debe ser mayor que cero"
        )

    return LLMConfig(
        url=url,
        model=model,
        timeout=timeout
    )

import logging

import requests

try:
    from .config import LLMConfig, load_llm_config
except ImportError:
    from config import LLMConfig, load_llm_config

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Error controlado al comunicarse con el modelo."""


class LLM:
    def __init__(
            self,
            config: LLMConfig | None = None
    ) -> None:
        config = config or load_llm_config()

        self.url = config.url
        self.model = config.model
        self.timeout = config.timeout


    def generate(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        logger.info(
            "Iniciando petición a Ollama model=%s timeout=%s",
            self.model,
            self.timeout
        )

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )
        except requests.Timeout as error:
            logger.error(
                "La petición a Ollama agotó el tiempo de espera"
            )
            raise LLMError(
                "Ollama ha tardado demasiado en responder."
            ) from error
        except requests.ConnectionError as error:
            raise LLMError(
                "No se pudo conectar con Ollama."
            ) from error

        logger.debug(
            "Ollama ha respondido con código HTTP %s",
            response.status_code
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise LLMError(
                "Ollama ha devuelto un error HTTP."
            ) from error

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as error:
            raise LLMError(
                "Ollama ha devuelto una respuesta inválida."
            ) from error

        if not isinstance(data, dict) or "response" not in data:
            raise LLMError(
                "Ollama ha devuelto una respuesta inválida."
            )

        response_text = data["response"]

        if not isinstance(response_text, str) or not response_text.strip():
            raise LLMError(
                "Ollama ha devuelto una respuesta inválida."
            )

        logger.info("Petición a Ollama completada")

        return response_text

import requests

try:
    from .config import LLMConfig, load_llm_config
except ImportError:
    from config import LLMConfig, load_llm_config


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
        
        print("Enviando petición...")

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )
        except requests.Timeout as error:
            raise LLMError(
                "Ollama ha tardado demasiado en responder."
            ) from error
        except requests.ConnectionError as error:
            raise LLMError(
                "No se pudo conectar con Ollama."
            ) from error

        print("Código: ", response.status_code)

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

        return response_text

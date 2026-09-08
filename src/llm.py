import requests

try:
    from .config import LLMConfig, load_llm_config
except ImportError:
    from config import LLMConfig, load_llm_config


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

        response = requests.post(
            self.url,
            json=payload,
            timeout=self.timeout
        )

        print("Código: ", response.status_code)

        response.raise_for_status()

        return response.json()["response"]
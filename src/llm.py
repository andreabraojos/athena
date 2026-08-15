import requests

class LLM:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen3:8b"

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
            timeout=120
        )

        print("Código: ", response.status_code)

        response.raise_for_status()

        return response.json()["response"]
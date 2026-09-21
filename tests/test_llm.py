import unittest
from unittest.mock import Mock, patch

import requests

from src.config import LLMConfig
from src.llm import LLM, LLMError


class TestLLM(unittest.TestCase):

    def test_uses_provided_configuration(self) -> None:
        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        self.assertEqual(
            llm.url,
            "http://servidor-prueba/api/generate"
        )
        self.assertEqual(llm.model, "modelo-prueba")
        self.assertEqual(llm.timeout, 30.0)

    @patch("src.llm.requests.post")
    def test_generate_sends_request_and_returns_response(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "response": "Respuesta simulada"
        }

        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertLogs("src.llm", level="DEBUG") as captured:
            result = llm.generate("Hola Athena")

        logs = "\n".join(captured.output)

        self.assertIn(
            "Iniciando petición a Ollama",
            logs
        )

        self.assertIn("modelo-prueba", logs)
        self.assertIn("timeout=30.0", logs)
        self.assertIn("código HTTP 200", logs)
        self.assertIn("Petición a Ollama completada", logs)
        self.assertNotIn("Hola Athena", logs)
        self.assertNotIn(config.url, logs)

        self.assertEqual(
                result,
                "Respuesta simulada"
        )

        mock_post.assert_called_once_with(
            "http://servidor-prueba/api/generate",
            json={
                "model": "modelo-prueba",
                "prompt": "Hola Athena",
                "stream": False
            },
            timeout=30.0
        )

        response.raise_for_status.assert_called_once_with()
        response.json.assert_called_once_with()

    @patch("src.llm.requests.post")
    def test_generate_translates_timeout_to_llm_error(
        self,
        mock_post
    ) -> None:
        mock_post.side_effect = requests.Timeout(
            "Tiempo agotado"
        )

        config = LLMConfig(
            url="http://servidor-prueba/api/generata",
            model="modelo-prueba",
            timeout=30.0
        )
        llm = LLM(config=config)

        with self.assertLogs("src.llm", level="ERROR") as captured:
            with self.assertRaisesRegex(
                LLMError,
                "Ollama ha tardado demasiado en responder"
            ):
                llm.generate("Hola Athena")

        logs = "\n".join(captured.output)

        self.assertIn(
            "La petición a Ollama agotó el tiempo de espera",
            logs
        )
        self.assertNotIn("Hola Athena", logs)
        self.assertNotIn(config.url, logs)

    @patch("src.llm.requests.post")
    def test_generate_translates_connection_error_to_llm_error(
        self,
        mock_post
    ) -> None:
        mock_post.side_effect = requests.ConnectionError(
            "Conexión rechazada"
        )

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "No se pudo conectar con Ollama"
        ):
            llm.generate("Hola Athena")

    @patch("src.llm.requests.post")
    def test_generate_translates_http_error_to_llm_error(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 500
        response.raise_for_status.side_effect = requests.HTTPError(
            "500 Server Error"
        )

        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto un error HTTP"
        ):
            llm.generate("Hola Athena")

    @patch("src.llm.requests.post")
    def test_generate_translates_invalid_json_error_to_llm_error(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.side_effect = requests.exceptions.JSONDecodeError(
            "JSON inválido.",
            "",
            0
        )

        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto una respuesta inválida."
        ):
            llm.generate("Hola Athena")

    @patch("src.llm.requests.post")
    def test_generate_translates_missing_response_to_llm_error(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {}
        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto una respuesta inválida."
        ):
            llm.generate("Hola Athena")

    @patch("src.llm.requests.post")
    def test_generate_rejects_non_string_response(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "response": None
        }
        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto una respuesta inválida."
        ):
            llm.generate("Hola Athena")

    @patch("src.llm.requests.post")
    def test_generate_rejects_blank_response(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "response": " "
        }
        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto una respuesta inválida."
        ):
            llm.generate("Hola Athena.")

    @patch("src.llm.requests.post")
    def test_generate_rejects_non_object_json_response(
        self,
        mock_post
    ) -> None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = []
        mock_post.return_value = response

        config = LLMConfig(
            url="http://servidor-prueba/api/generate",
            model="modelo-prueba",
            timeout=30.0
        )

        llm = LLM(config=config)

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha devuelto una respuesta inválida"
        ):
            llm.generate("Hola Athena")

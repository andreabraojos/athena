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

        result = llm.generate("Hola Athena")

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

        with self.assertRaisesRegex(
            LLMError,
            "Ollama ha tardado demasiado en responder"
        ):
            llm.generate("Hola Athena")

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

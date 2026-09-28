import unittest
from unittest.mock import Mock

from src.registry import ToolRegistry


class TestToolRegistry(unittest.TestCase):

    def test_execute_registered_command_returns_true(
            self
    ) -> None:
        registry = ToolRegistry()
        action = Mock()

        registry.register("memoria", action)

        handled = registry.execute("memoria")

        self.assertTrue(handled)
        action.assert_called_once_with()

    def test_execute_not_registered_command_returns_false(
            self
    ) -> None:
        registry = ToolRegistry()
        action = Mock()

        registry.register("memoria", action)

        handled = registry.execute("Hola")

        self.assertFalse(handled)
        action.assert_not_called()

    def test_execute_registered_command_with_argument(
            self
    ) -> None:
        registry = ToolRegistry()
        action = Mock()

        registry.register_with_argument("olvida", action)

        handled = registry.execute("Olvida Ciudad")

        self.assertTrue(handled)
        action.assert_called_once_with("Ciudad")

    def test_execute_command_without_argument_passes_empty_string(
            self
    ) -> None:
        registry = ToolRegistry()
        action = Mock()

        registry.register_with_argument("olvida", action)

        handled = registry.execute("olvida")

        self.assertTrue(handled)
        action.assert_called_once_with("")

    def test_execute_does_not_match_partial_command_name(
            self
    ) -> None:
        registry = ToolRegistry()
        action = Mock()

        registry.register_with_argument("olvida", action)

        handled = registry.execute("olvidado ciudad")

        self.assertFalse(handled)
        action.assert_not_called()

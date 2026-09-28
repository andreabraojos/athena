from collections.abc import Callable


class ToolRegistry:
    def __init__(self) -> None:
        self._methods: dict[str, Callable[[], None]] = {}
        self._methods_with_argument: dict[str, Callable[[str], None]] = {}

    def register(
            self,
            name: str,
            handler: Callable[[], None]
    ) -> None:
        self._methods[name] = handler

    def register_with_argument(
            self,
            name: str,
            handler: Callable[[str], None]
    ) -> None:
        self._methods_with_argument[name] = handler

    def execute(self, command: str) -> bool:
        original_command = command.strip()
        normalized_command = original_command.lower()

        action = self._methods.get(normalized_command)

        if action is not None:
            action()
            return True

        for name, handler in self._methods_with_argument.items():
            if normalized_command == name:
                argument = ""
            elif normalized_command.startswith(name + " "):
                argument = original_command[len(name):].strip()
            else:
                continue

            handler(argument)
            return True

        return False

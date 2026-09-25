from collections.abc import Callable


class ToolRegistry:
    def __init__(self) -> None:
        self._methods: dict[str, Callable[[], None]] = {}

    def register(
            self,
            name: str,
            handler: Callable[[], None]
    ) -> None:
        self._methods[name] = handler

    def execute(self, command: str) -> bool:
        action = self._methods.get(command)
        if action is None:
            return False

        action()
        return True
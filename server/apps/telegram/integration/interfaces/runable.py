from typing import Protocol


class Runable(Protocol):
    """Интерфейс запускаемого объекта."""

    def run(self) -> None:
        """Запуск."""

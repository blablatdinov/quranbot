from typing import Protocol


class UpdatesIteratorInterface(Protocol):
    """Интерфейс итератора по обновлениям."""

    def __iter__(self):
        """Точка входа в итератор."""

    def __next__(self) -> list[str]:
        """Вернуть следующий элемент."""

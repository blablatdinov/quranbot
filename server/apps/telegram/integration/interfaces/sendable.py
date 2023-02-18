from typing import Protocol


class SendableInterface(Protocol):
    """Интерфейс объекта, отправляющего ответы в API."""

    def send(self, update) -> list[dict]:
        """Отправка.

        :param update: Stringable
        """
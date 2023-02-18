from typing import Protocol


class UpdatesURLInterface(Protocol):
    """Интерфейс URL запроса для получения уведомлений."""

    def generate(self, update_id: int) -> str:
        """Генерация.

        :param update_id: int
        """
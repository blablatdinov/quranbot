from typing import final

from server.apps.telegram.integration.interfaces.stringable import Stringable


@final
class UnwrappedString(Stringable):
    """Строки без переноса."""

    def __init__(self, origin: Stringable):
        """Конструктор класса.

        :param origin: str
        """
        self._origin = origin

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return str(self._origin).replace('\n', '')

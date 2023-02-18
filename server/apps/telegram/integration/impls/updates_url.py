from typing import final

from server.apps.telegram.integration.interfaces.stringable import Stringable


@final
class UpdatesURL(Stringable):
    """Базовый URL обновлений из телеграма."""

    def __init__(self, token: str):
        """Конструктор класса.

        :param token: str
        """
        self._token = token

    def __str__(self):
        """Строчное представление.

        :return: str
        """
        return 'https://api.telegram.org/bot{0}/getUpdates'.format(self._token)
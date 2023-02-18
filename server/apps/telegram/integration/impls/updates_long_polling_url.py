from typing import final

import httpx

from server.apps.telegram.integration.interfaces.intable import Intable
from server.apps.telegram.integration.interfaces.updates_url import UpdatesURLInterface


@final
class UpdatesLongPollingURL(UpdatesURLInterface):
    """URL обновлений с таймаутом."""

    def __init__(self, updates_url: UpdatesURLInterface, long_polling_timeout: Intable):
        """Конструктор класса.

        :param updates_url: UpdatesURLInterface
        :param long_polling_timeout: Intable
        """
        self._origin = updates_url
        self._long_polling_timeout = long_polling_timeout

    def generate(self, update_id: int):
        """Генерация.

        :param update_id: int
        :return: str
        """
        return httpx.URL(self._origin.generate(update_id)).copy_add_param(
            'timeout',
            int(self._long_polling_timeout),
        )
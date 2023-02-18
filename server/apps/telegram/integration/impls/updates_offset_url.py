from typing import final

from server.apps.telegram.integration.interfaces.stringable import Stringable
from server.apps.telegram.integration.interfaces.updates_url import UpdatesURLInterface


@final
class UpdatesWithOffsetURL(UpdatesURLInterface):
    """URL для получения только новых обновлений."""

    def __init__(self, updates_url: Stringable):
        """Конструктор класса.

        :param updates_url: Stringable
        """
        self._updates_url = updates_url

    def generate(self, update_id: int):
        """Генерация.

        :param update_id: int
        :return: str
        """
        return '{0}?offset={1}'.format(self._updates_url, update_id)
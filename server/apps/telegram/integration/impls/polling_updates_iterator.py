import json
from typing import final

import httpx

from server.apps.telegram.integration.interfaces.intable import Intable
from server.apps.telegram.integration.interfaces.updates_interator import UpdatesIteratorInterface
from server.apps.telegram.integration.interfaces.updates_url import UpdatesURLInterface


@final
class PollingUpdatesIterator(UpdatesIteratorInterface):
    """Итератор по обновлениям."""

    def __init__(self, updates_url: UpdatesURLInterface, updates_timeout: Intable):
        """Конструктор класса.

        :param updates_url: UpdatesURLInterface
        :param updates_timeout: Intable
        """
        self._updates_url = updates_url
        self._offset = 0
        self._updates_timeout = updates_timeout

    def __iter__(self):
        """Точка входа в итератор.

        :return: PollingUpdatesIterator
        """
        return self

    def __next__(self) -> list[str]:
        """Вернуть следующий элемент.

        :return: list[Update]
        """
        with httpx.Client() as client:
            try:
                resp = client.get(
                    self._updates_url.generate(self._offset),
                    timeout=int(self._updates_timeout),
                )
            except httpx.ReadTimeout:
                return []
            resp_content = resp.text
            try:
                parsed_result = json.loads(resp_content)['result']
            except KeyError:
                return []
            if not parsed_result:
                return []
            self._offset = parsed_result[-1]['update_id'] + 1
            return [json.dumps(elem, ensure_ascii=False) for elem in parsed_result]
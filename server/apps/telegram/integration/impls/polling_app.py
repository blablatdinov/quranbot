from typing import final

from server.apps.telegram.integration.impls.polling_updates_iterator import PollingUpdatesIterator
from server.apps.telegram.integration.interfaces.runable import Runable
from loguru import logger

from server.apps.telegram.integration.interfaces.sendable import SendableInterface


@final
class PollingApp(Runable):
    """Приложение на long polling."""

    def __init__(self, updates: PollingUpdatesIterator, sendable: SendableInterface):
        """Конструктор класса.

        :param updates: PollingUpdatesIterator
        :param sendable: SendableInterface
        """
        self._sendable = sendable
        self._updates = updates

    def run(self) -> None:
        """Запуск."""
        logger.info('Start app on polling')
        for update_list in self._updates:
            for update in update_list:
                logger.debug('Update: {update}', update=update)
                self._sendable.send(update)
"""The MIT License (MIT).

Copyright (c) 2018-2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from typing import final

from loguru import logger

from server.apps.telegram.integration.impls.polling_updates_iterator import PollingUpdatesIterator
from server.apps.telegram.integration.interfaces.runable import Runable
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

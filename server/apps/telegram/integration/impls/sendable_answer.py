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
import json
from typing import final
from urllib import parse as url_parse

import httpx
from loguru import logger

from server.apps.telegram.integration.exceptions.internal import InternalBotError
from server.apps.telegram.integration.interfaces.sendable import SendableInterface
from server.apps.telegram.integration.interfaces.stringable import Stringable
from server.apps.telegram.integration.interfaces.tg_answer import TgAnswer


@final
class SendableAnswer(SendableInterface):
    """Объект, отправляющий ответы в API."""

    def __init__(self, answer: TgAnswer):
        """Конструктор класса.

        :param answer: TgAnswerInterface
        """
        self._answer = answer

    def send(self, update: Stringable) -> list[dict]:
        """Отправка.

        :param update: Stringable
        :return: list[str]
        :raises TelegramIntegrationsError: при невалидном ответе от API телеграмма
        """
        responses = []
        success_status = 200
        with httpx.Client() as client:
            for request in self._answer.build(update):
                logger.debug('Try send request to: {url}', url=url_parse.unquote(str(request.url)))
                resp = client.send(request)
                responses.append(resp.text)
                if resp.status_code != success_status:
                    raise InternalBotError(resp.text)
            return [json.loads(response) for response in responses]

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
                logger.debug('Try send request to: {0}'.format(url_parse.unquote(str(request.url))))
                resp = client.send(request)
                responses.append(resp.text)
                if resp.status_code != success_status:
                    raise InternalBotError(resp.text)
            return [json.loads(response) for response in responses]
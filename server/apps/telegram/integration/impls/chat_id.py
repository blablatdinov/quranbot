import re

from typing import final

from server.apps.telegram.integration.exceptions.internal import InternalBotError
from server.apps.telegram.integration.impls.unwrapped_string import UnwrappedString
from server.apps.telegram.integration.interfaces.intable import Intable
from server.apps.telegram.integration.interfaces.update import Update


@final
class TgChatId(Intable):

    def __init__(self, update: Update):
        self._update = update

    def __int__(self) -> int:
        """Числовое представление.

        :return: int
        :raises InternalBotError: В случае отсутсвия идентификатора чата в json
        """
        unwrapped_string = str(UnwrappedString(self._update))
        chat_json_object = re.search('chat"(:|: )({.+?})', unwrapped_string)
        if chat_json_object:
            return self._parse_id(chat_json_object)
        chat_json_object = re.search('from"(:|: )({.+?})', unwrapped_string)
        if chat_json_object:
            return self._parse_id(chat_json_object)
        raise InternalBotError

    def _parse_id(self, chat_json_object: re.Match) -> int:
        chat_id_regex_result = re.search(r'id"(:|: )(\d+)', chat_json_object.group(2))
        if not chat_id_regex_result:
            raise InternalBotError
        return int(chat_id_regex_result.group(2))

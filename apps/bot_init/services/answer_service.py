from typing import Any, Optional

from loguru import logger
from telebot.apihelper import ApiException

from apps.bot_init.markup import InlineKeyboard, Keyboard, get_default_keyboard
from apps.bot_init.models import Message
from apps.bot_init.utils import save_message


class Answer:
    """Класс-ответ возвращаемый в контроллеры."""

    text: str = None
    keyboard: Keyboard or InlineKeyboard = get_default_keyboard()
    tg_audio_id: str = None
    chat_id: int = None

    def __repr__(self) -> str:
        """Строковое представление."""
        return f'{self.text[:30]} (chat_id={self.chat_id})'

    def __init__(
        self,
        text: str = None,
        keyboard: Keyboard or InlineKeyboard = None,
        tg_audio_id: str = None,
        chat_id: int = None,
    ) -> None:
        if keyboard is None:
            keyboard = get_default_keyboard()
        self.text = text
        self.keyboard = keyboard
        self.tg_audio_id = tg_audio_id
        self.chat_id = chat_id

    def _send(self) -> Optional[Message]:
        from apps.bot_init.service import _subscriber_unsubscribed, send_message_to_admin
        from apps.bot_init.views import tbot
        try:
            if self.tg_audio_id:
                msg = tbot.send_audio(self.chat_id, audio=self.tg_audio_id)
            else:
                msg = tbot.send_message(self.chat_id, self.text, reply_markup=self.keyboard, parse_mode='HTML')
            message_instance = save_message(msg)
            return message_instance
        except ApiException as e:
            if 'bot was blocked by the user' in str(e) or 'user is deactivated' in str(e) or 'chat not found' in str(e):
                _subscriber_unsubscribed(self.chat_id)
            elif 'message text is empty' in str(e):  # TODO законченный контент отлавливается в рассылке сообщений
                send_message_to_admin('Закончился ежедневный контент')
                raise Exception('Закончился ежедневный контент')
            else:
                logger.error(e)
                send_message_to_admin(f'Непредвиденная ошибка\n\n{e}')
                raise e

    def check_chat_id(self) -> None:
        """Проверка идентификатора чата."""
        if self.chat_id is None:
            # TODO написать кастомный exception
            raise Exception(
                'Передайте chat_id либо при инициализации класса Answer либо при вызове метода send',
            )

    def send(self, chat_id: int = None) -> Message:
        """Отправляем ответ пользователю.

        Функция может принять как единственный экземпляр класса Answer, так и список экземпляров.
        Поэтому в функции нужна проверка
        """
        self.chat_id = self.chat_id or chat_id
        self.check_chat_id()
        message = self._send()
        return message


class AnswersList(list):
    """Список ответов."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(AnswersList, self).__init__(args)

    def send(self) -> None:
        """Метод для отправки сообщений."""
        for elem in self:
            elem.send()

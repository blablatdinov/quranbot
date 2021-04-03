from telebot.apihelper import ApiException
from loguru import logger

from apps.bot_init.markup import InlineKeyboard, Keyboard, get_default_keyboard
from apps.bot_init.utils import save_message


class Answer:
    text: str = None
    keyboard: Keyboard or InlineKeyboard = get_default_keyboard()
    tg_audio_id: str = None
    chat_id: int = None

    def __repr__(self):
        return f"{self.text[:30]} (chat_id={self.chat_id})"

    def __init__(
        self,
        text: str = None,
        keyboard: Keyboard or InlineKeyboard = None,
        tg_audio_id: str = None,
        chat_id: int = None,
    ):
        if keyboard is None:
            keyboard = get_default_keyboard()
        self.text = text
        self.keyboard = keyboard
        self.tg_audio_id = tg_audio_id
        self.chat_id = chat_id

    def _send(self):
        from apps.bot_init.service import send_message_to_admin, _subscriber_unsubscribed
        from apps.bot_init.views import tbot
        try:
            if self.tg_audio_id:
                msg = tbot.send_audio(self.chat_id, audio=self.tg_audio_id)
            else:
                msg = tbot.send_message(self.chat_id, self.text, reply_markup=self.keyboard, parse_mode="HTML")
            message_instance = save_message(msg)
            return message_instance
        except ApiException as e:
            if "bot was blocked by the user" in str(e) or "user is deactivated" in str(e) or "chat not found" in str(e):
                _subscriber_unsubscribed(self.chat_id)
            elif "message text is empty" in str(e):  # TODO законченный контент отлавливается в рассылке сообщений
                send_message_to_admin("Закончился ежедневный контент")
                raise Exception("Закончился ежедневный контент")
            else:
                logger.error(e)
                send_message_to_admin(f"Непредвиденная ошибка\n\n{e}")
                raise e

    def check_chat_id(self):
        if self.chat_id is None:
            raise Exception("Передайте chat_id либо при иницализации класса Answer либо при вызове метода send")  # TODO написать кастомный exception

    def send(self, chat_id: int = None):
        """Отправляем ответ пользователю.

        Функция может принять как единственный экземпляр класса Answer, так и список экземпляров.
        Поэтому в функции нужна проверка
        """
        self.chat_id = self.chat_id or chat_id
        self.check_chat_id()
        message = self._send()
        return message


class AnswersList(list):

    def __init__(self, *args, **kwargs):
        super(AnswersList, self).__init__(args)

    def send(self):
        for elem in self:
            elem.send()

"""Ошибки, возникающие при работе бота."""
from apps.bot_init.models import Message


class UnknownMessage(Exception):
    """Исключение вызывается если бот не знает как отвечать на это сообщение."""

    error_text: str

    def __init__(self, *args):
        """Обработка параметров при вызове исключения.

        Args:
            *args: ...
        """
        message = Message.objects.get(message_id=args[1])
        message.is_unknown = True
        message.save()
        self.error_text = args[0]

    def __str__(self):
        """Возвращает текст ошибки.

        Returns:
            return: ...
        """
        return self.error_text


class SuraDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данной суры."""

    pass


class AyatDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данного аята."""

    pass

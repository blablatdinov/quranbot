from bot_init.models import Message


class UnknownMessage(Exception):
    """Исключение вызывается если бот не знает как отвечать на это сообщение"""
    def __init__(self, *args):
        message = Message.objects.get(message_id=args[1])
        message.is_unknown = True
        message.save()
        self.value = args[0]

    def __str__(self):
        return self.value


class SuraDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данной суры"""
    pass


class AyatDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данного аята"""
    pass

class UnknownMessage(Exception):
    """Исключение вызывается если бот не знает как отвечать на это сообщение"""
    pass


class SuraDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данной суры"""
    pass


class AyatDoesNotExists(Exception):
    """Исключение вызывается если в базе данных нет данного аята"""
    pass

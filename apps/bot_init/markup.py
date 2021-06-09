"""Модуль, содержащий классы и функции для создания клавиатур."""
from telebot import types


class InlineKeyboard:
    """Класс создающий клавиатуру над строкой ввода сообщений."""

    def __init__(self, buttons):
        """Конструктор класса.

        Уровни вложенности:
        1. Все кнопки
        2. Строки
        3. Кнопки и их значения

        Args:
            buttons: ...

            example = tuple(
                tuple(tuple('button1', 'value1'), tuple('button2', 'value2')),
                tuple(tuple('button3', 'value3'),)

            )
        """
        self.keyboard = types.InlineKeyboardMarkup()
        lines = self.get_lines(buttons)
        for line in lines:
            self.keyboard.add(*line)

    def get_lines(self, buttons):
        """Метод для получения строк.

        Args:
            buttons: ...

        Yields:
            buttons_line: ...
        """
        for line in buttons:
            buttons_line = []
            for button_text in line:
                button = self.get_buttons(button_text)
                buttons_line.append(button)
            yield buttons_line

    def get_buttons(self, button_text):
        """Метод для получения кнопок.

        Args:
            button_text: ...

        Returns:
            return: ...
        """
        if isinstance(button_text, str):
            button = types.InlineKeyboardButton(text=button_text, callback_data=button_text)
        if isinstance(button_text, tuple):
            button = types.InlineKeyboardButton(text=button_text[0], callback_data=button_text[1])
        return button


class Keyboard:
    """Класс создающий клавиатуру под строкой ввода сообщений."""

    def __init__(self, buttons):
        """Конструктор класса.

        example = (
            ('button1', 'button2'),
            ('button3',)

        )

        Args:
            buttons: ...
        """
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lines = self.get_lines(buttons)
        for line in lines:
            self.keyboard.add(*line)

    def get_lines(self, buttons):
        """Метод для получения строк.

        Args:
            buttons: ...

        Yields:
            buttons_line: ...
        """
        for line in buttons:
            buttons_line = []
            for button_text in line:
                button = self.get_buttons(button_text)
                buttons_line.append(button)
            yield buttons_line

    def get_buttons(self, button_text):
        """Метод для получения кнопок.

        Args:
            button_text: ...

        Returns:
            return: ...
        """
        return types.KeyboardButton(button_text)


def get_default_keyboard(additional_buttons=None):
    """Функция возвращает дефолтную клавиатуру.

    Args:
        additional_buttons: ...

    Returns:
        return: ...
    """
    if additional_buttons is None:
        additional_buttons = []
    buttons = [
        ('🎧 Подкасты',),
        ('🕋 Время намаза',),
        ('🌟 Избранное', '🔍 Найти аят'),
    ] + additional_buttons
    return Keyboard(buttons).keyboard

"""Утилиты для работы бота."""
import json
import re
from datetime import datetime

from django.conf import settings
from django.utils.timezone import make_aware
from loguru import logger
from telebot import TeleBot

from apps.bot_init.models import CallbackData, Message


def save_message(msg):
    """Сохранение сообщения от пользователя."""
    logger.info("Saving message")
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = msg.json
    except Exception as e:  # TODO конкретизировать ошибку
        logger.error(f'{e}')
        json_str = str(msg)
    json_text = json.dumps(json_str, indent=2, ensure_ascii=False)
    message_instance = Message.objects.create(
        date=date,
        from_user_id=from_user_id,
        message_id=message_id,
        chat_id=chat_id,
        text=text,
        json=json_text,
    )
    return message_instance


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API."""
    return TeleBot(settings.TG_BOT.token, threaded=False)


def save_callback_data(call) -> CallbackData:
    """Функция для сохранения данных из inline кнопки."""
    logger.info("Saving callback data")
    date = make_aware(datetime.fromtimestamp(call.message.date))
    call_id = call.id
    chat_id = str(call.from_user.id)
    call_data = call.data
    json_ = str(call)
    json_ = re.sub(r"<telebot\.types\.User[^>]+>", f"'{settings.TG_BOT.name}'", json_)
    json_ = re.sub(r"<telebot\.types\.Chat[^>]+>", str(chat_id), json_)
    json_ = re.sub(r"<telebot\.types\.[^>]+>", "None", json_)
    try:
        json_ = eval(json_)
        json_ = json.dumps(json_, indent=2, ensure_ascii=False)
    except Exception as e:  # TODO конкретизировать
        logger.error(f'{e}')
        pass
    instance = CallbackData.objects.create(
        date=date,
        call_id=call_id,
        chat_id=chat_id,
        text=call_data,
        json=json_,
    )
    return instance


def stop_retry(func):
    """Декоратор, предотвращает повторный ответ на одно сообщение."""
    def wrapper(message):
        if Message.objects.filter(message_id=message.message_id):
            logger.error("Finding double message")
            return
        func(message)

    return wrapper

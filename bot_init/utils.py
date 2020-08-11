import re
import json

from datetime import datetime
from django.utils.timezone import make_aware
from bot_init.models import Message, CallbackData
from config.settings import TG_BOT


def save_message(msg):
    """ Сохранение сообщения от пользователя """
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = msg.json
    except:
        json_str = str(msg)
    json_text = json.dumps(json_str, indent=2, ensure_ascii=False)
    message_instance = Message.objects.create(date=date, from_user_id=from_user_id, message_id=message_id,
                           chat_id=chat_id, text=text, json=json_text)
    return message_instance


def save_callback_data(call) -> CallbackData:
    """Функция для сохранения данных из inline кнопки"""
    date = make_aware(datetime.fromtimestamp(call.message.date))
    call_id = call.id
    chat_id = call.from_user.id
    call_data = call.data
    json_ = str(call)
    json_ = re.sub(r'<telebot\.types\.User[^>]+>', f"'{TG_BOT.name}'", json_)
    json_ = re.sub(r'<telebot\.types\.Chat[^>]+>', str(chat_id), json_)
    json_ = eval(json_)
    json_text = json.dumps(json_, indent=2, ensure_ascii=False)
    instance = CallbackData.objects.create(
        date=date,
        call_id=call_id,
        chat_id=chat_id,
        text=call_data,
        json=json_text
    )
    return instance


def stop_retry(func):
    """Декоратор, предотвращает повторный ответ на одно сообщение"""
    def wrapper(message):
        if Message.objects.filter(message_id=message.message_id):
            return
            # TODO логгинг
        func(message)

    return wrapper

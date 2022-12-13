"""Утилиты для работы бота."""
import json
import re
import uuid
from datetime import datetime
from typing import Callable

import nats
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.utils.timezone import make_aware
from loguru import logger
from quranbot_schema_registry import validate_schema
from telebot import TeleBot, types

from apps.bot_init.models import CallbackData, Message


async def queue_sink(event_title: str, event_version: int, payload: dict) -> None:
    """Отправка событий в очередь.

    :param event_title: str
    :param event_version: int
    :param payload: dict
    """
    event = {
        'event_id': str(uuid.uuid4()),
        'event_version': event_version,
        'event_name': event_title,
        'event_time': str(datetime.now()),
        'producer': 'quranbot-django',
        'data': payload,
    }
    validate_schema(event, event_title, event_version)
    nats_client = await nats.connect(
        'nats://{0}:{1}'.format(settings.NATS_HOST, settings.NATS_PORT),
        token=settings.NATS_TOKEN,
    )
    js = nats_client.jetstream()
    queue_name = 'quranbot'
    await js.add_stream(name=queue_name)
    logger.info('Publishing to queue: {0}, event_id: {1}'.format(queue_name, event['event_id']))
    await js.publish(queue_name, json.dumps(event).encode('utf-8'))
    logger.info('Event: {0} to queue: {1} successful published'.format(event['event_id'], queue_name))
    await nats_client.close()


sync_queue_sync = async_to_sync(queue_sink)


def message_saved_event(msg: types.Message) -> None:
    """Отправить событие о сохранении сообщения.

    :param msg: types.Message
    """
    sync_queue_sync(
        'Messages.Created',
        1,
        {'messages': [{'message_json': json.dumps(msg.json)}]},
    )


def save_message(msg: types.Message) -> Message:
    """Сохранение сообщения от пользователя."""
    logger.info('Saving message')
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


async_save_message = sync_to_async(save_message)


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API."""
    return TeleBot(settings.TG_BOT.token, threaded=False)


def save_callback_data(call: types.CallbackQuery) -> CallbackData:
    """Функция для сохранения данных из inline кнопки."""
    logger.info('Saving callback data')
    date = make_aware(datetime.fromtimestamp(call.message.date))
    call_id = call.id
    chat_id = str(call.from_user.id)
    call_data = call.data
    json_ = str(call)
    json_ = re.sub(r'<telebot\.types\.User[^>]+>', f'"{settings.TG_BOT.name}"', json_)
    json_ = re.sub(r'<telebot\.types\.Chat[^>]+>', str(chat_id), json_)
    json_ = re.sub(r'<telebot\.types\.[^>]+>', 'None', json_)
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


def stop_retry(func: Callable) -> Callable:
    """Декоратор, предотвращает повторный ответ на одно сообщение."""
    def wrapper(message: types.Message) -> None:
        if Message.objects.filter(message_id=message.message_id):
            logger.error('Finding double message')
            return
        func(message)

    return wrapper

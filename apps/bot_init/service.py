"""Бизнес логика для взаимодействия с телеграмм."""
import os
from time import sleep
from typing import List

from django.conf import settings
from loguru import logger

from apps.bot_init.models import Admin, AdminMessage, Message, Subscriber, SubscriberAction
from apps.bot_init.schemas import SUBSCRIBER_ACTIONS
from apps.bot_init.services.answer_service import Answer, AnswersList
from apps.bot_init.services.subscribers import get_subscriber_by_chat_id
from apps.bot_init.utils import get_tbot_instance
from apps.content.models import MorningContent

SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = settings.BASE_DIR + '/deploy/quranbot-keys.json'
tbot = get_tbot_instance()


def delete_message_in_tg(chat_id: int, message_id: int) -> None:
    """Функция для удаления сообщения в телеграмм."""
    tbot.delete_message(chat_id, message_id)


def get_admins_list() -> List[int]:
    """Функция возвращает список администраторов."""
    return settings.TG_BOT.admins + [admin.subscriber.tg_chat_id for admin in Admin.objects.all()]


def send_message_to_admin(message_text: str) -> Message:
    """Отправляем сообщение админу."""
    answer = Answer(message_text)
    admins_tg_chat_ids = get_admins_list()
    for admin_tg_chat_id in admins_tg_chat_ids:
        message_instance = answer.send(admin_tg_chat_id)
    return message_instance


def update_webhook(host: str = f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}') -> None:
    """Обновляем webhook."""
    tbot.remove_webhook()
    sleep(1)
    tbot.set_webhook(host)
    logger.info(tbot.get_webhook_info())


def check_user_status_by_typing(chat_id: int) -> bool:
    """Определить подписан ли пользователь на бота, попробовав отправить сигнал о печати."""
    sub = get_subscriber_by_chat_id(chat_id)
    try:
        tbot.send_chat_action(sub.tg_chat_id, 'typing')
        if not sub.is_active:
            sub.is_active = True
            sub.save(update_fields=['is_active'])
        return True
    except Exception as e:
        if ('bot was blocked by the user' in str(e) or 'user is deactivated' in str(e)) and sub.is_active:
            _subscriber_unsubscribed(sub.tg_chat_id)


def count_active_users() -> int:
    """Подсчитать кол-во активных пользователей."""
    result = os.system('./check_users')
    return result


def _create_action(subscriber: Subscriber, action: str) -> None:
    """Создаем запись в БД о подписке, отписке или реактивации бота пользователем."""
    SubscriberAction.objects.create(subscriber=subscriber, action=action)


def _subscriber_unsubscribed(chat_id: int) -> None:
    """Действия, выполняемые при блокировке бота пользователем."""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.is_active = False
    subscriber.save()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[1][0])


def _not_created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Функция вызывается если пользователь, который уже существует в базе был корректно обработан."""
    if subscriber.is_active:
        return Answer('Вы уже зарегистрированы', chat_id=subscriber.tg_chat_id)
    _create_action(subscriber, SUBSCRIBER_ACTIONS[2][0])
    subscriber.is_active = True
    subscriber.save(update_fields=['is_active'])
    return Answer(f'Рады видеть вас снова, вы продолжите с дня {subscriber.day}', chat_id=subscriber.tg_chat_id)


def _created_subscriber_service(subscriber: Subscriber) -> List[Answer]:
    """Функция обрабатывает и генерирует ответ для нового подписчика."""
    start_message_text = AdminMessage.objects.get(key='start').text
    day_content = MorningContent.objects.get(day=1).content_for_day()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[0][0])
    answers = [
        Answer(start_message_text, chat_id=subscriber.tg_chat_id),
        Answer(day_content, chat_id=subscriber.tg_chat_id),
    ] + [
        Answer('Зарегистрировался новый пользователь.', chat_id=admin) for admin in get_admins_list()
    ]

    return AnswersList(*answers)

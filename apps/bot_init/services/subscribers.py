from typing import Optional

from loguru import logger

from apps.bot_init.models import Subscriber


def get_subscriber_by_chat_id(chat_id: int) -> Optional[Subscriber]:
    """Получить подписчика по идентификатору."""
    try:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        return subscriber
    except Subscriber.DoesNotExist:
        logger.info(f'Subscriber {chat_id} does not exist')

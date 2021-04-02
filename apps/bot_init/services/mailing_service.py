from loguru import logger

from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.services.answer_service import Answer


def do_mailing(text):
    mailing = Mailing.objects.create()
    for subscriber in Subscriber.objects.filter(is_active=True):
        logger.info(f"Send message to {subscriber.tg_chat_id}")
        Answer(text, chat_id=subscriber.tg_chat_id, mailing_instance=mailing).send()

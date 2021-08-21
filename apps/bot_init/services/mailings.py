from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.services.answer_service import Answer
from apps.bot_init.markup import get_default_keyboard


def execute_mailing(text: str):
    keyboard = get_default_keyboard()
    mailing = Mailing.objects.create()
    for subscriber in Subscriber.objects.filter(is_active=True):
        message_instance = Answer(text, chat_id=subscriber.tg_chat_id, keyboard=keyboard).send()
        message_instance.mailing = mailing
        message_instance.save(update_fields=['mailing'])

    return mailing

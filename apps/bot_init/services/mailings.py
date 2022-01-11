from apps.bot_init.markup import get_default_keyboard
from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.services.answer_service import Answer


def execute_mailing(text: str) -> Mailing:
    keyboard = get_default_keyboard()
    mailing = Mailing.objects.create()
    for subscriber in Subscriber.objects.filter(is_active=True):
        message_instance = Answer(text, chat_id=subscriber.tg_chat_id, keyboard=keyboard).send()
        if not message_instance:
            continue
        message_instance.mailing = mailing
        message_instance.save(update_fields=['mailing'])

    return mailing

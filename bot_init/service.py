from bot_init.models import Subscriber, AdminMessage
from content.models import MorningContent


def registration_subscriber(message):
    """ Логика сохранения подписчика """
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=message.chat.id)
    if not created:
        if subscriber.is_active:
            return ...
        subscriber.is_active = True
        subscriber.save(update_fields=['is_active'])
        return ...
    start_message_text = AdminMessage.objects.get(key='start').text
    day_content = MorningContent.objects.get(day=1)

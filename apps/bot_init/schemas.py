from typing import NamedTuple

from apps.bot_init.markup import InlineKeyboard, Keyboard, get_default_keyboard


class Answer(NamedTuple):
    text: str = None
    keyboard: Keyboard or InlineKeyboard = get_default_keyboard()
    tg_audio_id: str = None


SUBSCRIBER_ACTIONS = (
    ('subscribed', 'подписался'),
    ('unsubscribed',  'отписался'),
    ('reactivated', 'реактивировался'),
)

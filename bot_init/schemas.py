from typing import NamedTuple

from bot_init.markup import InlineKeyboard, Keyboard


class Answer(NamedTuple):
    text: str = None
    keyboard: Keyboard or InlineKeyboard = None
    tg_audio_id: str = None


SUBSCRIBER_ACTIONS = (
    ('subscribed', 'подписался'),
    ('unsubscribed',  'отписался'),
    ('reactivated', 'реактивировался'),
)

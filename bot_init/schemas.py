from typing import NamedTuple

from bot_init.markup import InlineKeyboard, Keyboard


class Answer(NamedTuple):
    text: str
    keyboard: Keyboard or InlineKeyboard = None


SUBSCRIBER_ACTIONS = (
    ('subscribed', 'подписался'),
    ('unsubscribed',  'отписался'),
    ('reactivated', 'реактивировался'),
)

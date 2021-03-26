import pytest
from mixer.backend.django import mixer

from apps.bot_init.service import get_referal_link

pytestmark = [pytest.mark.django_db]


def test_get_referal_link(subscriber):
    answer = get_referal_link(subscriber.tg_chat_id)

    assert answer.text == f"https://t.me/Quran_365_bot?start={subscriber.pk}"

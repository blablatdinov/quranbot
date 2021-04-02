import pytest
from mixer.backend.django import mixer

from apps.bot_init.services.text_message_service import text_message_service

pytestmark = [pytest.mark.django_db]


def test_button_service(subscriber):
    answer = text_message_service(subscriber.tg_chat_id, "Конкурс")

    assert "" in answer.text

import pytest
from django.conf import settings

from apps.bot_init.services.text_message_service import text_message_service
from apps.bot_init.models import AdminMessage

pytestmark = [pytest.mark.django_db]


def test_button_service(subscriber):
    answer = text_message_service(subscriber.tg_chat_id, "Конкурс")

    assert AdminMessage.objects.get(key="concourse").text in answer.text
    assert f"https://t.me/{settings.TG_BOT.name}?start={subscriber.pk}" in answer.text
    assert "Кол-во пользователей зарегистрировавшихся по вашей ссылке: " in answer.text

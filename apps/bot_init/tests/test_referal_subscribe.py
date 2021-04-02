import re

import pytest
import requests_mock
from django.conf import settings

from apps.bot_init.service import registration_subscriber
from apps.bot_init.models import Admin, Message, Subscriber, AdminMessage
from apps.bot_init.services.commands_service import StartCommandService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_referer(subscriber, referer_message_answer, message_answer, morning_content):
    answers = StartCommandService(892342789, f"/start", additional_info=str(subscriber.id))()

    assert Subscriber.objects.get(tg_chat_id=892342789).referer == subscriber
    assert answers[0].text == "По вашей реферальной ссылке произошла регистрация"
    assert answers[1].text == AdminMessage.objects.first().text
    assert answers[2].text == morning_content.content_for_day()
    assert answers[3].text == "Зарегестрировался новый пользователь."


def test_fake_referer(morning_content):
    answers = StartCommandService(892342789, f"/start", additional_info="7584")()

    assert Subscriber.objects.count() == 1
    assert Subscriber.objects.first().referer is None


def test_invalid_referal_link(referer_message_answer, message_answer, morning_content):
    StartCommandService(892342789, f"/start", additional_info="ijoajfe")()

    assert Subscriber.objects.count() == 1
    assert Subscriber.objects.first().referer is None

import re
import json

import pytest
from mixer.backend.django import mixer
import requests_mock
from django.conf import settings

from apps.bot_init.service import registration_subscriber
from apps.bot_init.models import Message, Subscriber

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_referer(subscriber, referer_message_answer, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=892342789"), text=message_answer)
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=" + str(subscriber.tg_chat_id)), text=referer_message_answer)

        registration_subscriber(892342789, subscriber.pk)

    assert Subscriber.objects.get(tg_chat_id=892342789).referer == subscriber
    assert Message.objects.filter(text="По вашей реферальной ссылке произошла регистрация").exists()

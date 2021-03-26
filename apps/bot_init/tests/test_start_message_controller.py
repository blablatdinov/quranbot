import json
import re

import pytest
from django.test import Client
import requests_mock
from mixer.backend.django import mixer

from django.conf import settings
from apps.bot_init.models import Message

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def webhook_data():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/start_message_webhook.json") as f:
        return json.load(f)


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/sended_after_message.json") as f:
        return json.load(f)


@pytest.fixture
def morning_content():
    c1 = mixer.blend("content.MorningContent", day=1)
    c2 = mixer.blend("content.MorningContent", day=2)
    mixer.blend("content.Ayat", one_day_content=c1)


def test_get_prayer_time_controller(webhook_data, morning_content, message_answer):
    c = Client()

    with requests_mock.Mocker() as m:

        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage\?chat_id=358.+"), json=message_answer)
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage\?chat_id=111.+"), json=message_answer)
        response = c.post(f'/bot_init/{settings.TG_BOT.token}', webhook_data, content_type="application/json")

    assert response.status_code == 200

    assert Message.objects.count() == 4
    assert Message.objects.all()[0].text == "/start"

import json
import re

import pytest
from django.test import Client
import requests_mock
from mixer.backend.django import mixer

from django.conf import settings
from apps.bot_init.models import Message, Subscriber
from apps.bot_init.services.commands_service import StartCommandService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_start_message_without_referal_service(morning_content, referer_message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=32984"), text=referer_message_answer)
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=358610865"), text=referer_message_answer)
        StartCommandService(32984, "/start")()

    assert Subscriber.objects.last().tg_chat_id == 32984


def test_start_message_with_referal_service(morning_content, subscriber, referer_message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=" + str(subscriber.tg_chat_id)), text=referer_message_answer)
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id=358610865"), text=referer_message_answer)
        StartCommandService(32984, f"/start", additional_info=str(subscriber.id))()

    assert Subscriber.objects.last().tg_chat_id == 32984
    assert Subscriber.objects.last().referer.id == subscriber.id

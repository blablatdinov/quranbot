import json
import re

import pytest
from django.test import Client
import requests_mock
from mixer.backend.django import mixer

from django.conf import settings
from apps.bot_init.models import Message, Subscriber
from apps.bot_init.services.commands_service import StartCommandService
from apps.bot_init.service import get_referals_count

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_start_message_with_referal_service(morning_content, subscriber):
    StartCommandService(32984, f"/start", additional_info=str(subscriber.id))()
    StartCommandService(98348, f"/start", additional_info=str(subscriber.id))()
    StartCommandService(93854, f"/start", additional_info=str(subscriber.id))()

    got = get_referals_count(subscriber)

    assert got == 3


def test_referers_count_after_deactivate_referer(morning_content, subscriber):
    StartCommandService(32984, f"/start", additional_info=str(subscriber.id))()
    Subscriber.objects.filter(tg_chat_id=32984).update(is_active=False)

    got = get_referals_count(subscriber)

    assert got == 0
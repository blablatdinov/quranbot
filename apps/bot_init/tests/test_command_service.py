import re

import requests_mock
import pytest
from mixer.backend.django import mixer
from django.conf import settings

from apps.bot_init.services.commands_service import CommandService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_command_service_without_additional_info(morning_content, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org.+chat_id="), text=message_answer)
        service = CommandService(83924, "/start")
        answer = service()

    assert service.additional_info is None


def test_getting_additional_info():
    service = CommandService(83924, "/start 1")
    service.get_additional_info()

    assert service.additional_info == "1"

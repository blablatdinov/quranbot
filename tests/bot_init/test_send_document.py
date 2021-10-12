import re

import pytest
import requests_mock
from mixer.backend.django import mixer

from apps.bot_init.services.handle_service import handle_query_service

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def document():
    return mixer.blend("content.File", name="PDF_ramadan_dairy")


@pytest.fixture(autouse=True)
def admin_messages():
    return mixer.blend("bot_init.AdminMessage", key="print_instructions")


def test(document, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage"), text=message_answer)
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendDocument"), text=message_answer)
        handle_query_service("accept_with_conditions", 9823474)

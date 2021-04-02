import re

import pytest
import requests_mock
from mixer.backend.django import mixer
from django.conf import settings

from apps.bot_init.services.answer_service import Answer
from apps.bot_init.models import Message

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def mailing():
    return mixer.blend("bot_init.Mailing")


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


def test_mailing_param_in_answer(mailing, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage\?chat_id=923453294"), text=message_answer)
        Answer("some text", chat_id=923453294, mailing_instance=mailing).send()

    assert Message.objects.last().mailing == mailing

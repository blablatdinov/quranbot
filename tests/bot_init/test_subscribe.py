import re

import pytest
import requests_mock
from django.conf import settings

from apps.bot_init.service import registration_subscriber

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/tests/bot_init/fixture/referer_message.json") as f:
        return f.read()


def test_registration(message_answer, morning_content):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"api.telegram.org"), text=message_answer)
        registration_subscriber(923842934)

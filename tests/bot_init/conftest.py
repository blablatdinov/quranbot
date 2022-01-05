import random

import pytest
import ujson
from django.conf import settings
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def morning_content():
    morning_content = mixer.blend('content.MorningContent', day=1)
    mixer.blend('content.Ayat', one_day_content=morning_content)
    return morning_content


@pytest.fixture()
def subscriber():
    return mixer.blend('bot_init.Subscriber')


@pytest.fixture
def message_answer():

    def _message_answer(message_id: int = None):
        if not message_id:
            message_id = random.randrange(9999)
        with open(f'{settings.BASE_DIR}/tests/bot_init/fixture/referer_message.json') as f:
            data = ujson.load(f)
            data['result']['message_id'] = message_id
            return ujson.dumps(data)

    return _message_answer

import json

import pytest
from django.conf import settings
from mixer.backend.django import mixer


@pytest.fixture
def large_content():
    return b"Saubuligiz!" * 5300000


@pytest.fixture
def small_content():
    return b"Saubuligiz!"


@pytest.fixture
def subscriber():
    return mixer.blend("bot_init.Subscriber", tg_chat_id=358610865)


@pytest.fixture
def tg_audio_answer():
    with open(f"{settings.BASE_DIR}/apps/content/tests/fixtures/tg_answer.json", "r") as f:
        data = json.load(f)
    return data
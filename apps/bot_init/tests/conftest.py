import pytest
from mixer.backend.django import mixer

from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def morning_content():
    morning_content = mixer.blend("content.MorningContent", day=1)
    mixer.blend("content.Ayat", one_day_content=morning_content)
    return morning_content


@pytest.fixture()
def subscriber():
    return mixer.blend("bot_init.Subscriber")


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()
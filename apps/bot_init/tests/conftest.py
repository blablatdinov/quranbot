import pytest
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def subscriber():
    morning_content = mixer.blend("content.MorningContent", day=1)
    mixer.blend("content.Ayat", one_day_content=morning_content)
    return mixer.blend("bot_init.Subscriber")

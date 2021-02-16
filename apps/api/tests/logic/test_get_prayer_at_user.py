from datetime import datetime

import pytest
from mixer.backend.django import mixer

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def chat_id():
    return 238492384


@pytest.fixture
def city():
    return mixer.blend("prayer.City", name="Жопинск")
 

@pytest.fixture()
def subscriber(chat_id, city):
    return mixer.blend("bot_init.Subscriber", tg_chat_id=chat_id, city=city)


@pytest.fixture()
def prayers_at_user(subscriber, city):
    mixer.cycle(5).blend(
        "prayer.PrayerAtUser",
        subscriber=subscriber,
        prayer__city=city,
        prayer__day__date=datetime.now(),
    )


def test_serialized_data_structure(chat_id, prayers_at_user):  # FIXME перенести в сериализаторы
    ...

def test_logic(chat_id, prayers_at_user):  # FIXME naming
    gotted = PrayerAtUserGenerator(chat_id)()
    prayer = gotted[0]
    assert prayer.city.name, "Жопинск"

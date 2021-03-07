from datetime import datetime
from random import randint

import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.prayer.schemas import PRAYER_NAMES

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def chat_id():
    return 234892342


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Мухосранск")


@pytest.fixture()
def subscriber(chat_id, city):
    return mixer.blend("bot_init.Subscriber", tg_chat_id=chat_id, city=city)


@pytest.fixture()
def subscriber_without_city(chat_id):
    return mixer.blend("bot_init.Subscriber", tg_chat_id=chat_id)


@pytest.fixture()
def prayers(city):
    for x in PRAYER_NAMES:
        prayer_name = x[0]
        mixer.blend("prayer.Prayer", name=prayer_name, city=city, day__date=datetime.today())
    return


@pytest.fixture()
def prayer_at_subscriber(subscriber, city):
    return [
        mixer.blend(
            "prayer.PrayerAtUser",
            subscriber=subscriber,
            prayer__name=x[0],
            prayer__day__date=datetime.today(),
            prayer__city=city,
        ) for x in PRAYER_NAMES
    ]


@pytest.fixture()
def daily_content():
    mixer.cycle(10).blend(
        "content.MorningContent", 
        day=(x for x in range(1, 11)),
        ayats=mixer.cycle(3).blend("content.Ayat")
    )
    mixer.cycle(30).blend(
        "bot_init.Subscriber",
        day=(randint(1, 10) for _ in range(30)),
        is_active=True
    )

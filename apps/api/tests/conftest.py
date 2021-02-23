from datetime import datetime

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

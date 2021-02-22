# FIXME тесты на получение для разных городов и пользователей
import re
from datetime import datetime

import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer

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
    for x in PRAYER_NAMES:
        prayer_name = x[0]
        mixer.blend(
            "prayer.PrayerAtUser", 
            subscriber=subscriber, 
            prayer__name=prayer_name,
            prayer__day__date=datetime.today(),
            prayer__city=city,
        )
    return 


def test_without_params(client):
    got = client.get("/api/v1/getPrayerTime")
    gotted_data = got.json()

    assert gotted_data.get("detail") == "Передайте chat_id или город."


def test_chat_id(client, subscriber, prayer_at_subscriber):
    got = client.get(f"/api/v1/getPrayerTime?chat_id={subscriber.tg_chat_id}")
    gotted_data = got.json()

    assert list(gotted_data.keys()) == ["city", "subscriber_chat_id", "sunrise_time", "prayers"]
    assert len(gotted_data.get("prayers")) == 5
    assert list(gotted_data.get("prayers")[0].keys()) == ["prayer_name", "prayer_time", "is_read"]
    assert [x.get("prayer_name") for x in gotted_data.get("prayers")] == ['Иртәнге', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert re.match(r"^\d{2}:\d{2}:\d{2}$", gotted_data.get("sunrise_time"))


def test_city(client, city, prayers):
    got = client.get(f"/api/v1/getPrayerTime?city=Мухосранск")
    gotted_data = got.json()

    assert list(gotted_data.keys()) == ["city", "sunrise_time", "prayers"]
    assert len(gotted_data.get("prayers")) == 5
    assert list(gotted_data.get("prayers")[0].keys()) == ["prayer_name", "prayer_time"]
    assert [x.get("prayer_name") for x in gotted_data.get("prayers")] == ['Иртәнге', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert re.match(r"^\d{2}:\d{2}:\d{2}$", gotted_data.get("sunrise_time"))


def test_subscriber_without_city(client, subscriber_without_city):
    got = client.get(f"/api/v1/getPrayerTime?chat_id={subscriber_without_city.tg_chat_id}")
    gotted_data = got.json()

    assert gotted_data.get("detail") == 'Пользователь не определил город.'

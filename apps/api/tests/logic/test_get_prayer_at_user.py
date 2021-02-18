from datetime import datetime

import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator
from apps.prayer.exceptions.subscriber_not_set_city import SubscriberNotSetCity

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
def subscriber_without_city(chat_id, city):
    mixer.cycle(5).blend("bot_init.Subscriber")
    return mixer.blend("bot_init.Subscriber", tg_chat_id=39842359)


@pytest.fixture()
def prayers_at_user(subscriber, city):
    mixer.cycle(5).blend(
        "prayer.PrayerAtUser",
        subscriber=subscriber,
        prayer__city=city,
        prayer__day__date=datetime.now(),
    )


@pytest.fixture()
def client():
    return APIClient()


def test_serialized_data_structure(chat_id, prayers_at_user, client):  # FIXME перенести в сериализаторы
    got = client.get(f"/api/v1/getPrayerAtUser/?chat_id={chat_id}")
    data = got.json()

    assert got.status_code == 200


def test_get_exist_prayer_times(chat_id, prayers_at_user, subscriber):
    gotted = PrayerAtUserGenerator(chat_id)()
    prayer = gotted[0]
    assert prayer.city.name, "Жопинск"


# def test_get_prayer_times_without_city(chat_id):
#     gotted = PrayerAtUserGenerator(chat_id)()
#     prayer = gotted[0]
#     assert prayer.city.name, "Жопинск"


# def test_get_prayer_with_non_exist_city(subscriber_without_city):
#     ...

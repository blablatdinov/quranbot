from datetime import datetime

import pytest
import requests_mock
from mixer.backend.django import mixer

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Владивосток")


@pytest.fixture()
def subscriber(city):
    return mixer.blend("bot_init.Subscriber", city=city)


@pytest.fixture()
def vladivostok_prayers(city):
    mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 20), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )
    mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 19), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )
    return mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 18), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )


@pytest.fixture
def nominatium_response():
    with open("apps/prayer/tests/fixtures/nominatium_vladivostok_search_response.json", "r") as f:
        return f.read()


@pytest.fixture
def geonames_response():
    with open("apps/prayer/tests/fixtures/geonames_vladivostok_timezone_response.json", "r") as f:
        return f.read()


@pytest.mark.freeze_time('2021-03-20 01:00:00')
def test_name(vladivostok_prayers, subscriber, nominatium_response, geonames_response):  # FIXME naming
    with requests_mock.Mocker() as m:
        m.get("https://nominatim.openstreetmap.org/search?q=%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%B2%D0%BE%D1%81%D1%82%D0%BE%D0%BA&format=json&limit=1", text=nominatium_response)
        m.get("http://api.geonames.org/timezoneJSON?lat=43.1150678&lng=131.8855768&username=blablatdinov", text=geonames_response)
        got = PrayerAtUserGenerator(chat_id=subscriber.tg_chat_id)()
    
    assert str(got.prayers[0].prayer.day.date) == "2021-03-19"

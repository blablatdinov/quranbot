# FIXME тесты на получение для разных городов и пользователей
import re
import json
import requests_mock

import pytest

pytestmark = [pytest.mark.django_db]


def test_without_params(client):
    got = client.get("/api/v1/getPrayerTime")
    gotted_data = got.json()

    assert gotted_data.get("detail") == "Передайте chat_id или город."


@pytest.fixture
def nominatium_response():
    with open("tests/prayers/fixtures/nominatium_kazan_search_response.json", "r") as f:
        return f.read()


@pytest.fixture
def geonames_response():
    with open("tests/prayers/fixtures/geonames_timezone_response.json", "r") as f:
        return f.read()


def test_chat_id(client, subscriber, prayer_at_subscriber, nominatium_response, geonames_response):
    with requests_mock.Mocker() as m:
        m.get("https://nominatim.openstreetmap.org/search?q=%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C&format=json&limit=1", text=nominatium_response)
        m.get("http://api.geonames.org/timezoneJSON?lat=55.7823547&lng=49.1242266&username=blablatdinov", text=geonames_response)
        got = client.get(f"/api/v1/getPrayerTime?chat_id={subscriber.tg_chat_id}")
    gotted_data = got.json()

    assert list(gotted_data.keys()) == ["city", "subscriber_chat_id", "sunrise_time", "prayers"]
    assert len(gotted_data.get("prayers")) == 5
    assert list(gotted_data.get("prayers")[0].keys()) == ["id", "prayer_name", "prayer_time", "is_read"]
    assert [x.get("prayer_name") for x in gotted_data.get("prayers")] == ['Иртәнге', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert re.match(r"^\d{2}:\d{2}:\d{2}$", gotted_data.get("sunrise_time"))


def test_city(client, city, prayers):
    got = client.get(f"/api/v1/getPrayerTime?city={city.name}")
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

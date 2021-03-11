# FIXME тесты на получение для разных городов и пользователей
import re

import pytest

pytestmark = [pytest.mark.django_db]


def test_without_params(client):
    got = client.get("/api/v1/getPrayerTime")
    gotted_data = got.json()

    assert gotted_data.get("detail") == "Передайте chat_id или город."


def test_chat_id(client, subscriber, prayer_at_subscriber):
    got = client.get(f"/api/v1/getPrayerTime?chat_id={subscriber.tg_chat_id}")
    gotted_data = got.json()

    assert list(gotted_data.keys()) == ["city", "subscriber_chat_id", "sunrise_time", "prayers"]
    assert len(gotted_data.get("prayers")) == 5
    assert list(gotted_data.get("prayers")[0].keys()) == ["id", "prayer_name", "prayer_time", "is_read"]
    assert [x.get("prayer_name") for x in gotted_data.get("prayers")] == ['Иртәнге', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert re.match(r"^\d{2}:\d{2}:\d{2}$", gotted_data.get("sunrise_time"))


def test_city(client, city, prayers):
    got = client.get("/api/v1/getPrayerTime?city=Мухосранск")
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

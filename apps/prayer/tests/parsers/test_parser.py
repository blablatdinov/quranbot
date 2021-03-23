from datetime import datetime

import pytest
from mixer.backend.django import mixer
import requests_mock
from django.conf import settings

from apps.prayer.parsers.ufa_prayer_time_parsers import PrayerTimeParser
from apps.prayer.models import Prayer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def page():
    with open(f"{settings.BASE_DIR}/apps/prayer/tests/fixtures/ufa_prayer_time_page.html") as f:
#/Users/almazilaletdinoots/quranbot/apps/prayer/tests/fixtures/ufa_prayer_time_page.html
        return f.read()


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Ufa")


def test_parser(page, city):
    with requests_mock.Mocker() as m:
        m.get("https://www.time-namaz.ru/85_ufa_vremy_namaza.html#month_time_namaz", text=page)
        PrayerTimeParser()()

    assert Prayer.objects.count() == 156
    assert [str(x[0]) for x in Prayer.objects.filter(day__date=datetime(2021, 3, 1)).values_list("time")] == ['06:20:00', '08:02:00', '13:30:00', '17:12:00', '18:55:00', '20:26:00']
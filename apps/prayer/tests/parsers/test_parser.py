from datetime import datetime

import pytest
from mixer.backend.django import mixer
import requests_mock
from django.conf import settings

from apps.prayer.parsers.ufa_prayer_time_parsers import PrayerTimeParser
from apps.prayer.models import Prayer

pytestmark = [pytest.mark.django_db]


def page(filename):
    with open(f"{settings.BASE_DIR}/apps/prayer/tests/fixtures/{filename}") as f:
        return f.read()


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Ufa")


def test_parser(city):
    with requests_mock.Mocker() as m:
        m.get("https://www.time-namaz.ru/85_ufa_vremy_namaza.html#month_time_namaz", text=page("ufa_prayer_time_page.html"))
        m.get("https://www.time-namaz.ru/85_ufa_vremy_namaza-next.html#month_time_namaz", text=page("ufa_prayer_time_next_page.html"))
        PrayerTimeParser()()
        
    assert Prayer.objects.count() == 306
    assert [str(x[0]) for x in Prayer.objects.filter(day__date=datetime(2021, 3, 1)).values_list("time")] == ['06:20:00', '08:02:00', '13:30:00', '17:12:00', '18:55:00', '20:26:00']
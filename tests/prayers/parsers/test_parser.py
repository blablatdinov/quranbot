import re
from datetime import datetime

import pytest
from mixer.backend.django import mixer
import requests_mock
from django.conf import settings

from apps.prayer.parsers.time_namaz_ru_parser import PrayerTimeParser
from apps.prayer.models import Prayer

pytestmark = [pytest.mark.django_db]


def page(filename):
    with open(f"{settings.BASE_DIR}/tests/prayers/fixtures/{filename}") as f:
        return f.read()


@pytest.fixture(autouse=True)
def cites():
    for x in ["Уфа", "Москва"]:
        mixer.blend("prayer.City", name=x)


@pytest.mark.parametrize("city_name", ["ufa", "moscow"])
def test_parser(city_name):
    with requests_mock.Mocker() as m:
        m.register_uri("GET", re.compile(r"https://www.time-namaz.ru/.+_vremy_namaza.html#month_time_namaz"), text=page("ufa_prayer_time_page.html"))
        m.register_uri("GET", re.compile(r"https://www.time-namaz.ru/.+_vremy_namaza-next.html#month_time_namaz"), text=page("ufa_prayer_time_next_page.html"))
        PrayerTimeParser(city_name=city_name)()
        
    assert Prayer.objects.count() == 306
    assert [str(x[0]) for x in Prayer.objects.filter(day__date=datetime(2021, 3, 1)).values_list("time")] == ['06:20:00', '08:02:00', '13:30:00', '17:12:00', '18:55:00', '20:26:00']
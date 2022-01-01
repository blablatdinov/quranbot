import re
from datetime import datetime

import pytest
from django.conf import settings
from mixer.backend.django import mixer

from apps.prayer.models import Prayer
from apps.prayer.parsers.time_namaz_ru_parser import PrayerTimeParser

pytestmark = [pytest.mark.django_db]


def page(filename):
    with open(f'{settings.BASE_DIR}/tests/prayers/fixtures/{filename}') as f:
        return f.read()


@pytest.fixture(autouse=True)
def cites():
    for x in ['Уфа', 'Москва']:
        mixer.blend('prayer.City', name=x)


@pytest.fixture()
def time_namaz_mock(http_mock):
    http_mock.register_uri(
        'GET',
        re.compile(r'https://www.time-namaz.ru/.+_vremy_namaza.html#month_time_namaz'),
        text=page('ufa_prayer_time_page.html'),
    )
    http_mock.register_uri(
        'GET',
        re.compile(r'https://www.time-namaz.ru/.+_vremy_namaza-next.html#month_time_namaz'),
        text=page('ufa_prayer_time_next_page.html'),
    )


@pytest.mark.freeze_time('2021-03-01')
@pytest.mark.parametrize('city_name', ['ufa', 'moscow'])
def test_parser(city_name, time_namaz_mock):
    PrayerTimeParser(city_name=city_name)()

    assert Prayer.objects.count() == 306
    assert (
        list(map(str, Prayer.objects.filter(day__date=datetime(2021, 3, 1)).values_list('time', flat=True))) ==
        ['06:20:00', '08:02:00', '13:30:00', '17:12:00', '18:55:00', '20:26:00']
    )

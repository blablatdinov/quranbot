from datetime import datetime

import pytest
import requests_mock
from django.conf import settings
from mixer.backend.django import mixer

from apps.prayer.models import Prayer
from apps.prayer.parsers.rt_prayer_time_parsers import PrayerTimeParser, get_time_by_str

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def city():
    mixer.blend('prayer.City', name='Зажопинск', link_to_csv='http://dumrt.ru/netcat_files/391/638/Zazhopinsk.csv')


@pytest.fixture()
def csv():
    with open(settings.BASE_DIR + '/tests/prayers/fixtures/Kazan.csv', 'rb') as f:
        return f.read()


def test_parser(city, csv):
    with requests_mock.Mocker() as m:
        m.get('http://dumrt.ru/netcat_files/391/638/Zazhopinsk.csv', content=csv)
        PrayerTimeParser()()

    assert Prayer.objects.count() == 144
    # assert False, Prayer.objects.count()


def test_get_time_by_str():
    assert datetime(2021, 2, 23) == get_time_by_str('23.02.2021')

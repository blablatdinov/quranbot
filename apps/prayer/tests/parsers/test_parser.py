import pytest
from mixer.backend.django import mixer
import requests_mock
from django.conf import settings

from apps.prayer.parsers.ufa_prayer_time_parsers import PrayerTimeParser

# pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def page():
    with open(f"{settings.BASE_DIR}/apps/prayer/tests/fixtures/ufa_prayer_time_page.html") as f:
#/Users/almazilaletdinoots/quranbot/apps/prayer/tests/fixtures/ufa_prayer_time_page.html
        return f.read()


def test_parser(page):
    with requests_mock.Mocker() as m:
        m.get("https://www.time-namaz.ru/85_ufa_vremy_namaza.html#month_time_namaz", text=page)
        assert False, PrayerTimeParser()()
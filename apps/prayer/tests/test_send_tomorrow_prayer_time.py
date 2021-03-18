import pytest
import requests_mock

from apps.prayer.service import send_prayer_time

pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time('2021-03-17')
def test_send_tomorrow_prayer_time(prayers):
    ...  # TODO доработать тест

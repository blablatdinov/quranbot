import pytest
import pytz

from apps.prayer.services.geography import get_city_timezone


@pytest.mark.parametrize('city_name,timezone', [
    ('Владивосток', 'Asia/Vladivostok'),
    ('Казань', 'Europe/Moscow'),
    ('Уфа', 'Asia/Yekaterinburg'),
])
def test_get_city_timezone(city_name, timezone):  # FIXME замокай это
    got = get_city_timezone(city_name)

    assert pytz.timezone(timezone) == got

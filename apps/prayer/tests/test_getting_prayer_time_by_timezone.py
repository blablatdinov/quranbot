from datetime import datetime

import pytest
from mixer.backend.django import mixer

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Владивосток")


@pytest.fixture()
def subscriber(city):
    return mixer.blend("bot_init.Subscriber", city=city)


@pytest.fixture()
def vladivostok_prayers(city):
    mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 20), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )
    mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 19), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )
    return mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 18), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )


@pytest.mark.freeze_time('2021-03-20 01:00:00')
def test_name(vladivostok_prayers, subscriber):  # FIXME naming
    got = PrayerAtUserGenerator(chat_id=subscriber.tg_chat_id)()
    
    assert str(got.prayers[0].prayer.day.date) == "2021-03-19"

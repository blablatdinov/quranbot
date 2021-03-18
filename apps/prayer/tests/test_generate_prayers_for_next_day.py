from datetime import datetime

import pytest
from mixer.backend.django import mixer

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator

pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time('2021-03-17')
def test_generate_prayers_for_next_day(prayers, subscriber):
    got = PrayerAtUserGenerator(chat_id=subscriber.tg_chat_id, day="tomorrow")()

    assert len(got.prayers) == 6
    assert [p.prayer.name for p in got.prayers] == ['Иртәнге', 'Восход', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert str(got.prayers[0].prayer.day.date) == "2021-03-18"

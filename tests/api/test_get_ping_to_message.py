from datetime import datetime

import pytest
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def message(mixer):
    mixer.blend('bot_init.Message', date=datetime(2021, 8, 2, 0, 0, 0), from_user_id=123)
    mixer.blend('bot_init.Message', date=datetime(2021, 8, 2, 0, 0, 2), from_user_id=settings.TG_BOT.id)
    mixer.blend('bot_init.Message', date=datetime(2021, 8, 2, 0, 1, 0), from_user_id=123)
    mixer.blend('bot_init.Message', date=datetime(2021, 8, 2, 0, 1, 4), from_user_id=settings.TG_BOT.id)


def test(client):
    got = client.get('/api/v1/get-ping-to-message/')

    assert got.status_code == 200
    assert got.json() == {'seconds': 3}

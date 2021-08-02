from datetime import datetime

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def messages(mixer):
    mixer.cycle(3).blend('bot_init.Message', from_user_id=333, date=datetime(2021, 7, 26))
    mixer.cycle(7).blend('bot_init.Message', from_user_id=333, date=datetime(2021, 7, 28))
    mixer.cycle(4).blend('bot_init.Message', from_user_id=333, date=datetime(2021, 7, 29))
    mixer.cycle(9).blend('bot_init.Message', from_user_id=333, date=datetime(2021, 7, 30))


def test(client):
    got = client.get('/api/v1/get-data-for-usage-graphic/?dates_range=2021-07-26,2021-07-30')

    assert got.status_code == 200
    assert got.json() == [
        {
            'date': '2021-07-26',
            'message_count': 3,
        },
        {
            'date': '2021-07-27',
            'message_count': 0,
        },
        {
            'date': '2021-07-28',
            'message_count': 7,
        },
        {
            'date': '2021-07-29',
            'message_count': 4,
        },
        {
            'date': '2021-07-30',
            'message_count': 9,
        },
    ]

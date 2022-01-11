import pendulum
import pytest

from apps.bot_init.models import Message

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def messages(mixer):
    Message.objects.all().delete()
    mixer.cycle(3).blend('bot_init.Message', from_user_id=333, date=pendulum.datetime(2021, 7, 26, tz='Europe/Moscow'))
    mixer.cycle(7).blend('bot_init.Message', from_user_id=333, date=pendulum.datetime(2021, 7, 28, tz='Europe/Moscow'))
    mixer.cycle(4).blend('bot_init.Message', from_user_id=333, date=pendulum.datetime(2021, 7, 29, tz='Europe/Moscow'))
    mixer.cycle(9).blend('bot_init.Message', from_user_id=333, date=pendulum.datetime(2021, 7, 30, tz='Europe/Moscow'))


def test(client, django_assert_max_num_queries):
    with django_assert_max_num_queries(1):
        got = client.get('/api/v1/bot/get-data-for-usage-graphic/?dates_range=2021-07-26,2021-07-30')

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

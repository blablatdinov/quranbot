import pendulum
import pytest
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def message(mixer):
    pendulum.datetime(2021, 8, 2, 0, 0, 0, tz='Europe/Moscow')
    for message_id, (user_id, date_time) in enumerate((
        (123,                pendulum.datetime(2021, 8, 2, 0, 0, 0, tz='Europe/Moscow')),  # noqa: E241
        (settings.TG_BOT.id, pendulum.datetime(2021, 8, 2, 0, 0, 2, tz='Europe/Moscow')),
        (123,                pendulum.datetime(2021, 8, 2, 0, 1, 0, tz='Europe/Moscow')),  # noqa: E241
        (settings.TG_BOT.id, pendulum.datetime(2021, 8, 2, 0, 1, 4, tz='Europe/Moscow')),
    ), start=1):
        mixer.blend(
            'bot_init.Message',
            date=date_time,
            from_user_id=user_id,
            message_id=message_id,
            mailing=None,
        )


@pytest.mark.freeze_time('2021-08-03')
def test(client):
    got = client.get('/api/v1/bot/get-ping-to-message/')

    assert got.status_code == 200
    assert got.json() == {'seconds': 3}

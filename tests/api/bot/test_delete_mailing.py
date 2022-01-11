import re

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def mailing(mixer):
    return mixer.blend('bot_init.Mailing')


@pytest.fixture()
def mock_telegram(http_mock):
    http_mock.register_uri(
        'POST',
        re.compile(r'https://api\.telegram\.org.+/deleteMessage.+'),
        json={'ok': True, 'result': True},
    )


@pytest.fixture(autouse=True)
def mailing_messages(mixer, mailing):
    return mixer.cycle(5).blend('bot_init.Message', mailing=mailing)


def test(client, django_assert_max_num_queries, mailing, mock_telegram):
    with django_assert_max_num_queries(4):
        got = client.delete(f'/api/v1/bot/mailings/{mailing.pk}/')

    mailing.refresh_from_db()

    assert got.status_code == 204
    assert mailing.is_cleaned is True

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def mailing(mixer):
    return mixer.blend('bot_init.Mailing')


@pytest.fixture(autouse=True)
def mailing_messages(mixer, mailing):
    return mixer.cycle(5).blend('bot_init.Message', mailing=mailing)


def test(client, django_assert_max_num_queries):
    with django_assert_max_num_queries(3):
        got = client.get('/api/v1/bot/mailings/')

    assert got.status_code == 200
    assert list(got.json()['results'][0].keys()) == ['id', 'is_cleaned', 'recipients_count']

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def messages(mixer):
    mailing = mixer.blend('bot_init.Mailing')
    mixer.cycle(3).blend('bot_init.Message', is_unknown=True, text='a', mailing=mailing)
    mixer.cycle(2).blend('bot_init.Message', is_unknown=False, text='a', mailing=mailing)
    mixer.cycle(4).blend('bot_init.Message', is_unknown=False, text='a')


def test_unknown(client):
    got = client.get('/api/v1/bot/messages/?is_unknown=false')

    payload = got.json()['results']

    assert len(payload) == 6


def test_known(client):
    got = client.get('/api/v1/bot/messages/?is_unknown=true')

    payload = got.json()['results']

    assert len(payload) == 3


def test_not_mailing(client):
    got = client.get('/api/v1/bot/messages/?in_mailing=false')

    payload = got.json()['results']

    assert len(payload) == 4

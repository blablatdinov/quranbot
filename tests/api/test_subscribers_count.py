import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def subscribers(mixer):
    mixer.blend('bot_init.Subscriber', is_active=True)
    mixer.blend('bot_init.Subscriber', is_active=True)
    mixer.blend('bot_init.Subscriber', is_active=True)
    mixer.blend('bot_init.Subscriber', is_active=True)
    mixer.blend('bot_init.Subscriber', is_active=False)
    mixer.blend('bot_init.Subscriber', is_active=False)
    mixer.blend('bot_init.Subscriber', is_active=False)


def test(client):
    got = client.get('/api/v1/get-subscribers-count/')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['active', 'all']

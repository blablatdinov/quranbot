import pytest

from apps.bot_init.models import Mailing

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def subscriber(mixer):
    return mixer.blend('bot_init.Subscriber', tg_chat_id=358610865, is_active=True)


def test(client):
    got = client.post('/api/v1/mailings/', data={
        'text': 'some text',
    })

    assert got.status_code == 201
    assert Mailing.objects.filter(pk=got.json()['id']).exists()

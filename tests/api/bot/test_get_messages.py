import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def messages(mixer):
    return mixer.cycle(10).blend('bot_init.Message', text='asdf' * 50)


def test(client):
    got = client.get('/api/v1/bot/messages/')

    payload = got.json()['results']

    assert got.status_code == 200
    assert list(payload[0]) == ['date', 'from_user_id', 'chat_id', 'mailing', 'is_unknown', 'text', 'message_id']
    assert payload[0]['text'] == 'asdfasdfasdfasdfasdf...'

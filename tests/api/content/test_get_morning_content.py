import pytest

from apps.content.models import MorningContent

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def ayats(mixer):
    content = mixer.blend('content.MorningContent')
    return mixer.cycle(15).blend('content.Ayat', one_day_content=content)


def test(client, ayats):
    got = client.get('/api/v1/morning-contents/')
    payload = got.json()['results']

    assert got.status_code == 200
    assert MorningContent.objects.count() > 0
    assert list(payload[0].keys()) == ['id', 'day', 'content_length', 'related_ayats']
    assert len(payload[0]['related_ayats']) == 15

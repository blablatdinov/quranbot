import pytest

from apps.content.models import MorningContent

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat(mixer):
    return mixer.blend('content.Ayat', content='s' * 5000)


def test(client, ayat):
    got = client.post('/api/v1/morning-contents/', data={
        'day': 1,
        'ayats_ids': [ayat.pk],
    })

    assert got.status_code == 400
    assert got.json()['content'][0] == 'max len of content should be less than 4096 symbols'
    assert MorningContent.objects.count() == 0

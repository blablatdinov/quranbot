import pytest

from apps.content.models import MorningContent, Ayat

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayats(mixer):
    return mixer.cycle(15).blend('content.Ayat')


def test(client, ayats):
    ayats_ids = [x.pk for x in ayats]
    got = client.post('/api/v1/morning-contents/', data={
        'day': 1,
        'ayats_ids': ayats_ids,
    })
    payload = got.json()

    assert got.status_code == 201
    assert MorningContent.objects.count() > 0
    assert list(payload.keys()) == ['id', 'related_ayats']
    assert Ayat.objects.filter(one_day_content__pk=payload['id']).count() == 15

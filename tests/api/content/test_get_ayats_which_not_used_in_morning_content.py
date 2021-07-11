import pytest
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def ayats():
    mixer.cycle(7).blend(
        'content.Ayat',
        one_day_content=mixer.blend('content.MorningContent')
    )
    mixer.cycle(3).blend(
        'content.Ayat',
    )


def test(client):
    got = client.get('/api/v1/get-not-used-ayats/')

    assert got.status_code == 200
    assert len(got.json()['results']) == 3
    assert list(got.json()['results'][0].keys()) == [
        'id',
        'additional_content',
        'content',
        'arab_text',
        'trans',
        'sura',
        'ayat',
        'link',
    ]

import pytest
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat():
    return mixer.blend('content.Ayat')


def test(ayat, client):
    got = client.get(f'/api/v1/getAyat/{ayat.pk}/')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['id', 'additional_content', 'content', 'arab_text', 'trans', 'sura', 'ayat']

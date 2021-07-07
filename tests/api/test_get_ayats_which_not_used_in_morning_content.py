import pytest
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayats():
    return mixer.blend('content.Ayat')


def test(client):
    got = client.get('/api/v1/get-not-used-ayats')

    assert got.status_code == 200

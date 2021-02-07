import pytest
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.mark.parametrize("sura,ayat,status", [
    (1, 2, 200),
])
def test_get_sura(client, sura, ayat, status):
    response = client.get(f'/api/v1/getAyat/')

    assert response.status_code == 200
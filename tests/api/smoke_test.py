import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client():
    return APIClient()


@pytest.mark.parametrize("sura,ayat,status", [
    (1, 2, 200),
])
def test_get_sura(client, sura, ayat, status):
    response = client.post(f'/api/v1/getAyat?sura={sura}&ayat={ayat}')

    assert response.status_code == 200

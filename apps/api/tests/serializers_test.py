import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def ayat():
    return mixer.blend("content.Ayat")


@pytest.mark.parametrize("field", [
    "additional_content",
])
def test_get_sura(ayat, client, field):
    response = client.get(f'/api/v1/getAyat/').json()

    assert field in response.get("results")[0]
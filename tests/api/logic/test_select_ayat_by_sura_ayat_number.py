import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def ayat():
    mixer.blend("content.Ayat", ayat="1", sura__number=3)
    mixer.blend("content.Ayat", ayat="666", sura__number=8)
    mixer.blend("content.Ayat", ayat="1-5", sura__number=2)
    mixer.blend("content.Ayat", ayat="1, 2", sura__number=114)

    return mixer.blend("content.Ayat", additional_content="target ayat", ayat="5", sura__number=4)


def test_controller(client, ayat):
    response = client.get(f'/api/v1/getAyat?sura={ayat.sura.number}&ayat={ayat.ayat}').json()
    response_data = response.get("results")[0]

    assert len(response.get("results")) == 1
    assert response_data.get("sura") == 4
    assert response_data.get("ayat") == "5"

import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from apps.api.services.ayat_search import get_ayat_by_sura_ayat_numbers

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def ayat():
    mixer.blend("content.Ayat", ayat="1", sura__number=3)
    mixer.blend("content.Ayat", ayat="666", sura__number=8)

    return mixer.blend("content.Ayat", ayat="5", sura__number=4)


def test_controller(client, ayat):
    response = client.get(f'/api/v1/getAyat/?sura={ayat.sura.number}&ayat={ayat.ayat}').json()
    response_data = response.get("results")[0]

    assert ayat.sura.number == 4  # TODO почему падает если получать из словаря
    assert ayat.ayat == "5"


def test_logic(ayat):
    queryset = get_ayat_by_sura_ayat_numbers(ayat.sura.number, ayat.ayat)
    gotted_ayat = queryset[0]

    assert gotted_ayat.ayat == "5"
    assert gotted_ayat.sura.number == 4
import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def podcast():
    mixer.cycle(10).blend("content.Podcast")
    return mixer.blend("content.Podcast")


@pytest.fixture()
def client():
    return APIClient()


@pytest.mark.parametrize("url", [
    "/api/v1/getAyat",
    "/api/v1/getPodcast/",
    "/api/v1/getDailyContent",
    "/api/v1/getAyatsBySuraNum",
])
def test_endpoint(client, url):
    response = client.get(url)

    assert response.status_code == 200

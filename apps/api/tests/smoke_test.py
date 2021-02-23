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


def test_get_sura(client):
    response = client.get('/api/v1/getAyat/')

    assert response.status_code == 200


def test_get_random_podcast(client, podcast):
    response = client.get('/api/v1/getPodcast/')

    assert response.status_code == 200

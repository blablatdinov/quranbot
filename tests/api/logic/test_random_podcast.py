import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.content.services.podcast_services import get_random_podcast

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def podcast():
    mixer.cycle(10).blend("content.Podcast")
    return mixer.blend("content.Podcast")


def test_controller(client, podcast):
    gotted = client.get("/api/v1/getPodcast/")
    data = gotted.json().get("results")[0]

    assert list(data.keys()) == ["title", "audio"]
    assert list(data.get("audio").keys()) == ["link_to_file", "tg_file_id"]


def test_randomize_in_controller(client, podcast):
    prev_result = None
    flag = False
    for _ in range(50):
        gotted = client.get("/api/v1/getPodcast/?order=random").json().get("results")
        flag = prev_result != gotted[0]
        prev_result = gotted[0]

    assert len(gotted) == 1
    assert flag


def test_get_random_podcast(podcast):
    """Тест получения случайного подкаста.

    Тест может упасть из-за чудес рандома, попробуйте перезапустить тест
    """
    prev_result = None
    flag = False
    for _ in range(50):
        gotted_podcast = get_random_podcast()
        flag = prev_result != gotted_podcast
        prev_result = gotted_podcast

    assert flag

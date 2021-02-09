import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer

from apps.content.services.ayat_search import get_ayat_by_sura_ayat_numbers, AyatSearcher
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
    gotted = client.get("/api/v1/getPodcast/").json().get("results")[0]

    assert list(gotted.keys()) == ["title", "audio"]
    assert list(gotted.get("audio").keys()) == ["audio_link", "tg_file_id"]


def test_randomize_in_controller(client, podcast):
    prev_result = None
    flag = False
    for _ in range(5):
        gotted = client.get("/api/v1/getPodcast/?order=random").json().get("results")[0]
        flag = prev_result != gotted
        prev_result = gotted

    assert len(gotted) == 1
    assert flag


def test_get_random_podcast(podcast):
    """Тест получения случайного подкаста.

    Тест может упасть из-за чудес рандома, попробуйте перезапустить тест
    """
    prev_result = None
    flag = False
    for _ in range(5):
        gotted_podcast = get_random_podcast()
        flag = prev_result != gotted_podcast
        prev_result = gotted_podcast

    assert flag

import pytest
import requests_mock

from apps.content.models import File, Podcast
from apps.content.podcast_parser import PodcastParser

pytestmark = [pytest.mark.django_db]


def test_download_and_send_large_files(large_content):
    with requests_mock.Mocker() as m:

        m.get('https://nifiga-sebe.mp3', content=large_content)
        
        parser = PodcastParser()
        parser.title = 'Самый полезный подкаст'
        parser.link_to_file = 'https://nifiga-sebe.mp3'
        parser.article_link = 'https://nifiga-sebe.ru'
        parser.download_and_send_audio_file()
        parser.create_podcast()

    assert Podcast.objects.count() == 1
    assert File.objects.count() == 1
    assert Podcast.objects.first().audio.tg_file_id is None
    assert Podcast.objects.first().audio.link_to_file == 'https://nifiga-sebe.mp3'
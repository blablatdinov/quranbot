import re

import pytest
import requests_mock

from apps.content.models import File, Podcast
from apps.content.podcast_parser import PodcastParser

pytestmark = [pytest.mark.django_db]


def test_download_small_after_large(small_content, large_content, subscriber, tg_audio_answer):
    with requests_mock.Mocker() as m:

        m.get("https://nifiga-sebe.mp3", content=large_content)
        m.get("https://small.mp3", content=small_content)
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendAudio\?"), json=tg_audio_answer)
        
        parser = PodcastParser()
        parser.sub = subscriber

        parser.title = "Самый полезный подкаст"
        parser.link_to_file = "https://small.mp3"
        parser.article_link = "https://nifiga-sebe.ru"
        parser.download_and_send_audio_file()
        parser.create_podcast()

        parser.title = "Огромный себе размерчик"
        parser.link_to_file = "https://nifiga-sebe.mp3"
        parser.article_link = "https://nifiga-sebe.ru"
        parser.download_and_send_audio_file()
        parser.create_podcast()


    assert Podcast.objects.count() == 2
    assert File.objects.count() == 2
    assert Podcast.objects.first().audio.tg_file_id == "CQACAgIAAxkDAAIshWBGRaJwdieNTKufqZc4m9XAw12jAAIXCwACIyQ4SqTy0Yzg179WHgQ"
    assert Podcast.objects.last().audio.tg_file_id is None
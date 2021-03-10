import re
import pytest
import requests_mock
from mixer.backend.django import mixer
from django.conf import settings
from jinja2 import Template

from apps.content.podcast_parser import PodcastParser
from apps.content.models import Podcast

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def subscriber():
    return mixer.blend("bot_init.Subscriber", tg_chat_id=358610865)


def get_html(file_name):
    with open(f"{settings.BASE_DIR}/apps/content/tests/fixtures/{file_name}", "r") as f:
        return f.read()


def get_podcast(podcast_title: str = "Как терпеть?"):
    with open(f"{settings.BASE_DIR}/apps/content/tests/fixtures/podcast_single.html", "r") as f:
        return Template(f.read()).render(podcast_title=podcast_title)

def get_audio():
    with open(f"{settings.BASE_DIR}/apps/content/tests/fixtures/empty.mp3", "rb") as f:
        return f.read()


def tg_audio_answer():
    data = {
        "ok": True,
        "result": {
            'message_id': 11397, 
            'from': {
                'id': 452230948, 
                'is_bot': True, 
                'first_name': 'WokeUpSmiled', 
                'username': 'WokeUpSmiled_bot'
            }, 
            'chat': {
                'id': 358610865, 
                'first_name': 'Алмаз', 
                'last_name': 'Илалетдинов', 
                'username': 'ilaletdinov', 
                'type': 'private'
            }, 
            'date': 1615218082, 
            'audio': {
                'duration': 0, 
                'file_name': 'audio', 
                'mime_type': 'audio/mpeg', 
                'performer': 'Шамиль Аляутдинов', 
                'file_id': 'CQACAgIAAxkDAAIshWBGRaJwdieNTKufqZc4m9XAw12jAAIXCwACIyQ4SqTy0Yzg179WHgQ', 
                'file_unique_id': 'AgADFwsAAiMkOEo', 
                'file_size': 417
            }
        }
    }
    return data


def test_parse_podasts(subscriber):
    with requests_mock.Mocker() as m:
        m.get("https://umma.ru/audlo/shamil-alyautdinov/", text=get_html("podcasts_page.html"))
        m.get("https://umma.ru/audlo/shamil-alyautdinov/page/2", text=get_html("podcasts_page.html"))
        m.get("https://umma.ru/audlo/shamil-alyautdinov/page/3", status_code=404)

        m.get("https://umma.ru/kak-terpet/", text=get_podcast())
        m.get("https://umma.ru/dela-i-molitva-hadis/", text=get_podcast())
        m.get("https://umma.ru/tavassul-salyafiti/", text=get_podcast())
        m.get("https://umma.ru/tavassul-sufii/", text=get_podcast())
        m.get("https://umma.ru/tavassul-9-punktov/", text=get_podcast())
        m.get("https://umma.ru/tavassul-uchenie-al-azhara/", text=get_podcast())
        m.get("https://umma.ru/skolko-u-tebya-veri/", text=get_podcast())
        m.get("https://umma.ru/muzika--eto-haram/", text=get_podcast())
        m.get("https://umma.ru/tavassul-chto-nelzya/", text=get_podcast())
        m.get("https://umma.ru/tavassul-chto-mozhno/", text=get_podcast())

        m.get("https://umma.ru/uploads/audio/t2b2gsqq5b.mp3", content=get_audio())
        m.post("https://api.telegram.org/bot452230948:AAF4k2UPJ9yiG_E8Nhx3ovWyVQVy4F4J6SM/sendAudio?chat_id=358610865&performer=%D0%A8%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C+%D0%90%D0%BB%D1%8F%D1%83%D1%82%D0%B4%D0%B8%D0%BD%D0%BE%D0%B2", json=tg_audio_answer())
        
        PodcastParser()()

    assert Podcast.objects.count() == 20
    assert Podcast.objects.first().audio.tg_file_id == "CQACAgIAAxkDAAIshWBGRaJwdieNTKufqZc4m9XAw12jAAIXCwACIyQ4SqTy0Yzg179WHgQ"
    assert Podcast.objects.first().audio.audio_link == "https://umma.ru/uploads/audio/t2b2gsqq5b.mp3"
    assert Podcast.objects.first().title == "Как терпеть?"


def test_parse_new_podcasts(subscriber):
    with requests_mock.Mocker() as m:
        m.get("https://umma.ru/audlo/shamil-alyautdinov/", text=get_html("podcast_2_page.html"))
        m.get("https://umma.ru/audlo/shamil-alyautdinov/page/2", status_code=404)

        m.get("https://umma.ru/nevezhestvo-muzika-tavassul/", text=get_podcast("nevezhestvo-muzika-tavassul"))
        m.get("https://umma.ru/prosit-u-sheiha-ili-net/", text=get_podcast("prosit-u-sheiha-ili-net"))
        m.get("https://umma.ru/zastupnichestvo-kak-eto/", text=get_podcast("zastupnichestvo-kak-eto"))
        m.get("https://umma.ru/zhizn-prekrasna/", text=get_podcast("zhizn-prekrasna"))
        m.get("https://umma.ru/suicid-predotvrati/", text=get_podcast("suicid-predotvrati"))
        m.get("https://umma.ru/vozmozhnosti-mozga/", text=get_podcast("vozmozhnosti-mozga"))
        m.get("https://umma.ru/o-hristianstve/", text=get_podcast("o-hristianstve"))
        m.get("https://umma.ru/itog/", text=get_podcast("itog"))
        m.get("https://umma.ru/o-boge/", text=get_podcast("o-boge"))
        m.get("https://umma.ru/vse-vo-blago/", text=get_podcast("vse-vo-blago"))

        m.get("https://umma.ru/uploads/audio/t2b2gsqq5b.mp3", content=get_audio())
        m.post("https://api.telegram.org/bot452230948:AAF4k2UPJ9yiG_E8Nhx3ovWyVQVy4F4J6SM/sendAudio?chat_id=358610865&performer=%D0%A8%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C+%D0%90%D0%BB%D1%8F%D1%83%D1%82%D0%B4%D0%B8%D0%BD%D0%BE%D0%B2", json=tg_audio_answer())
        
        PodcastParser()()
        print(1)

    with requests_mock.Mocker() as m:
        m.get("https://umma.ru/audlo/shamil-alyautdinov/", text=get_html("podcasts_page.html"))
        m.get("https://umma.ru/audlo/shamil-alyautdinov/page/2", text=get_html("podcast_2_page.html"))
        m.get("https://umma.ru/audlo/shamil-alyautdinov/page/3", status_code=404)

        m.get("https://umma.ru/kak-terpet/", text=get_podcast("kak-terpet"))
        m.get("https://umma.ru/dela-i-molitva-hadis/", text=get_podcast("dela-i-molitva-hadis"))
        m.get("https://umma.ru/tavassul-salyafiti/", text=get_podcast("tavassul-salyafiti"))
        m.get("https://umma.ru/tavassul-sufii/", text=get_podcast("tavassul-sufii"))
        m.get("https://umma.ru/tavassul-9-punktov/", text=get_podcast("tavassul-9-punktov"))
        m.get("https://umma.ru/tavassul-uchenie-al-azhara/", text=get_podcast("tavassul-uchenie-al-azhara"))
        m.get("https://umma.ru/skolko-u-tebya-veri/", text=get_podcast("skolko-u-tebya-veri"))
        m.get("https://umma.ru/muzika--eto-haram/", text=get_podcast("muzika--eto-haram"))
        m.get("https://umma.ru/tavassul-chto-nelzya/", text=get_podcast("tavassul-chto-nelzya"))
        m.get("https://umma.ru/tavassul-chto-mozhno/", text=get_podcast("tavassul-chto-mozhno"))
        m.post("https://api.telegram.org/bot452230948:AAF4k2UPJ9yiG_E8Nhx3ovWyVQVy4F4J6SM/sendAudio?chat_id=358610865&performer=%D0%A8%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C+%D0%90%D0%BB%D1%8F%D1%83%D1%82%D0%B4%D0%B8%D0%BD%D0%BE%D0%B2", json=tg_audio_answer())
        
        PodcastParser()()
        print(2)

    assert Podcast.objects.count() == 20

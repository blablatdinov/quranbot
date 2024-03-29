# TODO добавить тестов, чтоб не спарсить лишнего
import random
import re

import pytest
import requests_mock
import ujson
from django.conf import settings
from jinja2 import Template

from apps.content.models import Podcast
from apps.content.podcast_parser import PodcastParser

pytestmark = [pytest.mark.django_db]


def get_html(file_name):
    with open(f'{settings.BASE_DIR}/tests/content/fixtures/{file_name}', 'r') as f:
        return f.read()


def get_podcast(podcast_title: str = None):
    if podcast_title is None:
        podcast_title = 'Как терпеть?'
        podcast_link_to_file = 'https://umma.ru/uploads/audio/t2b2gsqq5b.mp3'
    else:
        podcast_link_to_file = 'https://umma.ru/uploads/audio/t2b2gsqq5b.mp3'

    with open(f'{settings.BASE_DIR}/tests/content/fixtures/podcast_single.html', 'r') as f:
        return Template(f.read()).render(podcast_title=podcast_title, podcast_link_to_file=podcast_link_to_file)


def get_audio():
    with open(f'{settings.BASE_DIR}/tests/content/fixtures/empty.mp3', 'rb') as f:
        return f.read()


@pytest.fixture()
def tg_audio_answer():

    def _tg_audio_answer(request, context):
        context.status_code = 200
        with open(f'{settings.BASE_DIR}/tests/content/fixtures/tg_answer.json', 'r') as f:
            data = ujson.load(f)
            data['result']['message_id'] = random.randrange(9999)
        return ujson.dumps(data)

    return _tg_audio_answer


@pytest.fixture()
def podcasts_mock(http_mock, tg_audio_answer):
    http_mock.get('https://umma.ru/audlo/shamil-alyautdinov/page/1', text=get_html('podcasts_page.html'))
    http_mock.get('https://umma.ru/audlo/shamil-alyautdinov/page/2', status_code=404)

    http_mock.get('https://umma.ru/kak-terpet/', text=get_podcast())
    http_mock.get('https://umma.ru/dela-i-molitva-hadis/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-salyafiti/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-sufii/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-9-punktov/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-uchenie-al-azhara/', text=get_podcast())
    http_mock.get('https://umma.ru/skolko-u-tebya-veri/', text=get_podcast())
    http_mock.get('https://umma.ru/muzika--eto-haram/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-chto-nelzya/', text=get_podcast())
    http_mock.get('https://umma.ru/tavassul-chto-mozhno/', text=get_podcast())

    http_mock.get('https://umma.ru/uploads/audio/t2b2gsqq5b.mp3', content=get_audio())
    http_mock.register_uri('POST', re.compile(r'https://api.telegram.org/bot.+/sendAudio\?'), text=tg_audio_answer)


def test_parse_podasts(subscriber, podcasts_mock):
    PodcastParser()()

    assert Podcast.objects.count() == 10
    assert (
        Podcast.objects.first().audio.tg_file_id ==
        'CQACAgIAAxkDAAIshWBGRaJwdieNTKufqZc4m9XAw12jAAIXCwACIyQ4SqTy0Yzg179WHgQ'
    )
    assert Podcast.objects.first().audio.link_to_file == 'https://umma.ru/uploads/audio/t2b2gsqq5b.mp3'
    assert Podcast.objects.first().title == 'Как терпеть?'


def test_parse_new_podcasts(subscriber, tg_audio_answer):
    with requests_mock.Mocker() as m:
        m.get('https://umma.ru/audlo/shamil-alyautdinov/page/1', text=get_html('podcast_2_page.html'))
        m.get('https://umma.ru/audlo/shamil-alyautdinov/page/2', status_code=404)

        m.get('https://umma.ru/nevezhestvo-muzika-tavassul/', text=get_podcast('nevezhestvo-muzika-tavassul'))
        m.get('https://umma.ru/prosit-u-sheiha-ili-net/', text=get_podcast('prosit-u-sheiha-ili-net'))
        m.get('https://umma.ru/zastupnichestvo-kak-eto/', text=get_podcast('zastupnichestvo-kak-eto'))
        m.get('https://umma.ru/zhizn-prekrasna/', text=get_podcast('zhizn-prekrasna'))
        m.get('https://umma.ru/suicid-predotvrati/', text=get_podcast('suicid-predotvrati'))
        m.get('https://umma.ru/vozmozhnosti-mozga/', text=get_podcast('vozmozhnosti-mozga'))
        m.get('https://umma.ru/o-hristianstve/', text=get_podcast('o-hristianstve'))
        m.get('https://umma.ru/itog/', text=get_podcast('itog'))
        m.get('https://umma.ru/o-boge/', text=get_podcast('o-boge'))
        m.get('https://umma.ru/vse-vo-blago/', text=get_podcast('vse-vo-blago'))

        m.get('https://umma.ru/uploads/audio/t2b2gsqq5b.mp3', content=get_audio())
        m.register_uri('POST', re.compile(r'https://api.telegram.org/bot.+/sendAudio\?'), text=tg_audio_answer)

        PodcastParser()()

    with requests_mock.Mocker() as m:
        m.get('https://umma.ru/audlo/shamil-alyautdinov/page/1', text=get_html('podcasts_page.html'))
        m.get('https://umma.ru/audlo/shamil-alyautdinov/page/2', text=get_html('podcast_2_page.html'))
        m.get('https://umma.ru/audlo/shamil-alyautdinov/page/3', status_code=404)
        m.get('https://umma.ru/uploads/audio/t2b2gsqq5b.mp3', content=get_audio())

        m.get('https://umma.ru/nevezhestvo-muzika-tavassul/', text=get_podcast('nevezhestvo-muzika-tavassul'))
        m.get('https://umma.ru/prosit-u-sheiha-ili-net/', text=get_podcast('prosit-u-sheiha-ili-net'))
        m.get('https://umma.ru/zastupnichestvo-kak-eto/', text=get_podcast('zastupnichestvo-kak-eto'))
        m.get('https://umma.ru/zhizn-prekrasna/', text=get_podcast('zhizn-prekrasna'))
        m.get('https://umma.ru/suicid-predotvrati/', text=get_podcast('suicid-predotvrati'))
        m.get('https://umma.ru/vozmozhnosti-mozga/', text=get_podcast('vozmozhnosti-mozga'))
        m.get('https://umma.ru/o-hristianstve/', text=get_podcast('o-hristianstve'))
        m.get('https://umma.ru/itog/', text=get_podcast('itog'))
        m.get('https://umma.ru/o-boge/', text=get_podcast('o-boge'))
        m.get('https://umma.ru/vse-vo-blago/', text=get_podcast('vse-vo-blago'))

        m.get('https://umma.ru/kak-terpet/', text=get_podcast('kak-terpet'))
        m.get('https://umma.ru/dela-i-molitva-hadis/', text=get_podcast('dela-i-molitva-hadis'))
        m.get('https://umma.ru/tavassul-salyafiti/', text=get_podcast('tavassul-salyafiti'))
        m.get('https://umma.ru/tavassul-sufii/', text=get_podcast('tavassul-sufii'))
        m.get('https://umma.ru/tavassul-9-punktov/', text=get_podcast('tavassul-9-punktov'))
        m.get('https://umma.ru/tavassul-uchenie-al-azhara/', text=get_podcast('tavassul-uchenie-al-azhara'))
        m.get('https://umma.ru/skolko-u-tebya-veri/', text=get_podcast('skolko-u-tebya-veri'))
        m.get('https://umma.ru/muzika--eto-haram/', text=get_podcast('muzika--eto-haram'))
        m.get('https://umma.ru/tavassul-chto-nelzya/', text=get_podcast('tavassul-chto-nelzya'))
        m.get('https://umma.ru/tavassul-chto-mozhno/', text=get_podcast('tavassul-chto-mozhno'))
        m.register_uri('POST', re.compile(r'https://api.telegram.org/bot.+/sendAudio\?'), text=tg_audio_answer)

        PodcastParser()()

    assert Podcast.objects.count() == 20

import re
from datetime import datetime, timedelta
from datetime import time

import pytest
from mixer.backend.django import mixer
import requests_mock

from apps.bot_init.services.answer_service import Answer
from apps.prayer.service import send_prayer_time, get_prayer_time_or_no
from apps.bot_init.models import Message
from apps.prayer.models import Prayer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def subscriber(city):
    return mixer.blend("bot_init.Subscriber", city=city)


def test_saving(message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage"), json=message_answer)  # send prayers
        Answer("some text", chat_id=32490, comment="important comment").send()

    assert Message.objects.last().comment == "important comment"


@pytest.mark.freeze_time('2021-03-18 01:00:00')
def test(message_answer, subscriber, prayers):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage"), json=message_answer)  # send prayers
        answer = get_prayer_time_or_no(subscriber.tg_chat_id)
        answer.send(subscriber.tg_chat_id)

    assert Message.objects.last().comment == "update_iftar_time"
    assert "Время до ифтара" in answer.text


@pytest.mark.freeze_time('2021-03-18 01:00:34')
def test_calculate_time(message_answer, subscriber, prayers):
    p = Prayer.objects.filter(name="Ахшам").first()
    p.time = time(16, 32)
    p.save()

    answer = get_prayer_time_or_no(subscriber.tg_chat_id)
    answer.send(subscriber.tg_chat_id)

    assert f"Время до ифтара:" in answer.text
    assert f"Время до ифтара: 15:31:26" in answer.text


@pytest.mark.freeze_time('2021-03-18 15:21:43')
def test_calculate_short_time(message_answer, subscriber, prayers):
    p = Prayer.objects.filter(name="Ахшам").first()
    p.time = time(16, 32)
    p.save()

    answer = get_prayer_time_or_no(subscriber.tg_chat_id)
    answer.send(subscriber.tg_chat_id)

    assert f"Время до ифтара:" in answer.text
    assert f"Время до ифтара: 01:10:17" in answer.text


@pytest.mark.freeze_time('2021-03-18 17:15:00')
def test_calculate_time_after_iftar(message_answer, subscriber, prayers):
    p = Prayer.objects.filter(name="Ахшам").first()
    p.time = time(16, 32)
    p.save()

    answer = get_prayer_time_or_no(subscriber.tg_chat_id)
    answer.send(subscriber.tg_chat_id)

    assert f"Время до ифтара:" in answer.text
    assert f"Время до ифтара: 00:00:00" in answer.text
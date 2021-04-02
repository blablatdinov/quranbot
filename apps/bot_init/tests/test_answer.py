import re

import pytest
from mixer.backend.django import mixer
from django.conf import settings
import requests_mock

from apps.bot_init.services.answer_service import Answer, AnswersList
from apps.bot_init.models import Message

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/apps/bot_init/tests/fixture/referer_message.json") as f:
        return f.read()


@pytest.fixture
def answer(subscriber):
    return Answer(text="wow", chat_id=subscriber.tg_chat_id)


@pytest.fixture
def answer_without_chat_id():
    return Answer(text="wow")


@pytest.fixture
def answer_list(subscriber):
    return AnswersList(
        Answer(text="wow", chat_id=subscriber.tg_chat_id), 
        Answer(text="wow2", chat_id=subscriber.tg_chat_id),
        Answer(text="wow3", chat_id=subscriber.tg_chat_id),
    )


def test_answer_with_chat_id_sending(answer, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(f"api.telegram.org.+chat_id={answer.chat_id}"), text=message_answer)
        answer.send()

    assert Message.objects.count() == 1


def test_set_chat_id_by_method(subscriber, answer_without_chat_id, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(f"api.telegram.org.+chat_id={subscriber.tg_chat_id}"), text=message_answer)
        answer_without_chat_id.send(subscriber.tg_chat_id)

    assert Message.objects.count() == 1


def test_sending_without_chat_id(answer_without_chat_id):
    with pytest.raises(Exception) as exc:
        answer_without_chat_id.send()

        assert "Передайте chat_id либо при иницализации класса Answer либо при вызове метода send" in str(exc)


def test_answer_list_sending(answer_list, message_answer):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(f"api.telegram.org.+chat_id="), text=message_answer)
        answer_list.send()

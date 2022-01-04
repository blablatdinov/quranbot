import re

import pytest

from apps.bot_init.models import Message
from apps.bot_init.services.answer_service import Answer, AnswersList

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def answer(subscriber):
    return Answer(text='wow', chat_id=subscriber.tg_chat_id)


@pytest.fixture
def answer_without_chat_id():
    return Answer(text='wow')


@pytest.fixture
def answer_list(subscriber):
    return AnswersList(
        Answer(text='wow', chat_id=subscriber.tg_chat_id),
        Answer(text='wow2', chat_id=subscriber.tg_chat_id),
        Answer(text='wow3', chat_id=subscriber.tg_chat_id),
    )


def test_answer_with_chat_id_sending(answer, message_answer, http_mock):
    http_mock.register_uri('POST', re.compile(f'api.telegram.org.+chat_id={answer.chat_id}'), text=message_answer(100))
    answer.send()

    assert Message.objects.count() == 1


def test_set_chat_id_by_method(subscriber, answer_without_chat_id, message_answer, http_mock):
    http_mock.register_uri(
        'POST', re.compile(f'api.telegram.org.+chat_id={subscriber.tg_chat_id}'), text=message_answer(200),
    )
    answer_without_chat_id.send(subscriber.tg_chat_id)

    assert Message.objects.count() == 1


def test_sending_without_chat_id(answer_without_chat_id):
    with pytest.raises(Exception) as exc:
        answer_without_chat_id.send()

        assert 'Передайте chat_id либо при инициализации класса Answer либо при вызове метода send' in str(exc)


def test_answer_list_sending(answer_list, message_answer, http_mock):
    http_mock.register_uri('POST', re.compile('api.telegram.org.+chat_id=.+text=wow'), text=message_answer(300))
    http_mock.register_uri('POST', re.compile('api.telegram.org.+chat_id=.+text=wow2'), text=message_answer(400))
    http_mock.register_uri('POST', re.compile('api.telegram.org.+chat_id=.+text=wow3'), text=message_answer(500))
    answer_list.send()

import pytest
from django.conf import settings

from apps.bot_init.models import AdminMessage, Subscriber
from apps.bot_init.services.commands_service import StartCommandService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f'{settings.BASE_DIR}/tests/bot_init/fixture/referer_message.json') as f:
        return f.read()


@pytest.fixture
def message_answer():
    with open(f'{settings.BASE_DIR}/tests/bot_init/fixture/referer_message.json') as f:
        return f.read()


def test_referer(subscriber, referer_message_answer, message_answer, morning_content):
    answers = StartCommandService(892342789, '/start', additional_info=str(subscriber.tg_chat_id))()

    assert Subscriber.objects.get(tg_chat_id=892342789).referer == subscriber
    assert answers[0].text == 'По вашей реферальной ссылке произошла регистрация'
    assert answers[1].text == AdminMessage.objects.first().text
    assert answers[2].text == morning_content.content_for_day()
    assert answers[3].text == 'Зарегистрировался новый пользователь.'


def test_fake_referer(morning_content):
    StartCommandService(892342789, '/start', additional_info='7584')()

    assert Subscriber.objects.count() == 1
    assert Subscriber.objects.first().referer is None


def test_invalid_referal_link(referer_message_answer, message_answer, morning_content):
    StartCommandService(892342789, '/start', additional_info='ijoajfe')()

    assert Subscriber.objects.count() == 1
    assert Subscriber.objects.first().referer is None


def test_referal_subscribe_in_reactivation_case(subscriber, morning_content):
    StartCommandService(892342789, '/start')()
    subscriber = Subscriber.objects.last()
    subscriber.is_active = False
    subscriber.save()
    StartCommandService(892342789, '/start', additional_info=str(subscriber.tg_chat_id))()

    assert subscriber.referer is None

import pytest

from apps.bot_init.models import AdminMessage, Subscriber
from apps.bot_init.service import get_admins_list
from apps.bot_init.services.commands_service import StartCommandService

pytestmark = [pytest.mark.django_db]


def test_start_message_without_referal_service(morning_content):
    answers = StartCommandService(32984, '/start')()

    assert Subscriber.objects.last().tg_chat_id == 32984
    assert answers[0].text == AdminMessage.objects.first().text
    assert answers[1].text == morning_content.content_for_day()


def test_registration_after_deleting(morning_content):
    StartCommandService(32984, '/start')()
    Subscriber.objects.all().delete()
    answers = StartCommandService(32984, '/start')()

    assert Subscriber.objects.last().tg_chat_id == 32984
    assert answers[0].text == AdminMessage.objects.first().text
    assert answers[1].text == morning_content.content_for_day()
    assert len(answers) == 2 + len(get_admins_list())


def test_start_message_with_referal_service(morning_content, subscriber):
    StartCommandService(32984, '/start', additional_info=str(subscriber.id))()

    assert Subscriber.objects.last().tg_chat_id == 32984
    assert Subscriber.objects.last().referer.id == subscriber.id


def test_active_user_start_command(subscriber):
    answers = StartCommandService(subscriber.tg_chat_id, '/start')()

    assert answers[0].text == 'Вы уже зарегистрированы'
    assert len(answers) == 1

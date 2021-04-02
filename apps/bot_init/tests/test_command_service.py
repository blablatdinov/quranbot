import pytest

from apps.bot_init.services.commands_service import CommandService
from apps.bot_init.services.answer_service import AnswersList

pytestmark = [pytest.mark.django_db]


def test_command_service_without_additional_info(morning_content):
    service = CommandService(83924, "/start")
    answers = service()

    assert service.additional_info is None
    assert list(set([hasattr(x, "chat_id") for x in answers]))[0] == True
    assert type(answers) is AnswersList


def test_getting_additional_info():
    service = CommandService(83924, "/start 1")
    service.get_additional_info()

    assert service.additional_info == "1"

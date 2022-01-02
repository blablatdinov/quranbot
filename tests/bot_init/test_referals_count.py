import pytest
from django.conf import settings

from apps.bot_init.models import Subscriber
from apps.bot_init.services.commands_service import StartCommandService
from apps.bot_init.services.concourse import get_referals_count

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def referer_message_answer():
    with open(f'{settings.BASE_DIR}/tests/bot_init/fixture/referer_message.json') as f:
        return f.read()


def test_start_message_with_referal_service(morning_content, subscriber):
    StartCommandService(32984, '/start', additional_info=str(subscriber.id))()
    StartCommandService(98348, '/start', additional_info=str(subscriber.id))()
    StartCommandService(93854, '/start', additional_info=str(subscriber.id))()

    got = get_referals_count(subscriber)

    assert got == 3


def test_referers_count_after_deactivate_referer(morning_content, subscriber):
    StartCommandService(32984, '/start', additional_info=str(subscriber.id))()
    Subscriber.objects.filter(tg_chat_id=32984).update(is_active=False)

    got = get_referals_count(subscriber)

    assert got == 0

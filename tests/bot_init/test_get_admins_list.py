import re

from dotenv import load_dotenv
import pytest

from apps.bot_init.service import _subscriber_unsubscribed, _not_created_subscriber_service, _created_subscriber_service
from apps.bot_init.service import *
from apps.bot_init.service import _create_action
from apps.bot_init.models import *
from apps.bot_init.schemas import Answer
from apps.content.models import Sura
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def admin_in_db():
    s = Subscriber.objects.create(tg_chat_id=123)
    return Admin.objects.create(subscriber=s)

@pytest.fixture
def admins_from_env():
    load_dotenv('.env')
    admins = [
        int(chat_id) for chat_id in os.getenv('ADMINS').split(',')
    ]    
    return admins

def test_get_admins_list(admins_from_env, admin_in_db):
    admins_from_func = get_admins_list()
    expected_list = admins_from_env + [admin_in_db.subscriber.tg_chat_id]

    assert admins_from_func == expected_list
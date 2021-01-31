import os

import pytest
from dotenv import load_dotenv

from apps.bot_init.models import Admin, Subscriber
from apps.bot_init.service import get_admins_list

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def admin_in_db():
    s = Subscriber.objects.create(tg_chat_id=123)
    return Admin.objects.create(subscriber=s)


@pytest.fixture
def admins_from_env():
    load_dotenv(".env")
    admins = [
        int(chat_id) for chat_id in os.getenv("ADMINS").split(",")
    ]
    return admins


def test_get_admins_list(admins_from_env, admin_in_db):
    admins_from_func = get_admins_list()
    expected_list = admins_from_env + [admin_in_db.subscriber.tg_chat_id]

    assert admins_from_func == expected_list

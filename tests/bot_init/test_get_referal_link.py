import pytest
from django.conf import settings

from apps.bot_init.services.concourse import get_referal_link

pytestmark = [pytest.mark.django_db]


def test_get_referal_link(subscriber):
    got = get_referal_link(subscriber)

    assert f'https://t.me/{settings.TG_BOT.name}?start={subscriber.pk}' in got

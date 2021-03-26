import pytest
from mixer.backend.django import mixer

from apps.bot_init.service import registration_subscriber

pytestmark = [pytest.mark.django_db]


def test_registration():
    registration_subscriber(923842934)

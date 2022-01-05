import pytest
from mixer.backend.django import mixer

from apps.bot_init.services.text_message_service import text_message_service

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def podcast():
    return mixer.blend('content.Podcast')


def test(podcast):
    answer = text_message_service(24932804, 'Подкасты')

    assert answer.text == podcast.audio.link_to_file

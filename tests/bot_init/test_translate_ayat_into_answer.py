import pytest

from apps.bot_init.services.answer_service import AnswersList
from apps.bot_init.services.text_message_service import translate_ayat_into_answer

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def audio_file(mixer):
    return mixer.blend('content.File')


@pytest.fixture()
def ayat(mixer, audio_file):
    res = mixer.blend('content.Ayat', sura__number=1, ayat='1', audio=audio_file)
    mixer.blend('content.Ayat', sura__number=1, ayat='2')
    return res


def test(ayat):
    got = translate_ayat_into_answer(ayat)

    assert isinstance(got, AnswersList)

import pytest

from apps.bot_init.markup import InlineKeyboard
from apps.bot_init.services.text_message_service import get_keyboard_for_ayat

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat(mixer):
    first = mixer.blend('content.Ayat', ayat=1, sura__number=1)
    mixer.blend('content.Ayat', ayat=1, sura__number=2)
    return first


def test(ayat):
    got = get_keyboard_for_ayat(ayat)
    expected_keyboard = InlineKeyboard(
        (
            (('Добавить в избранное', 'add_in_favourites(1)'),),
            (('2:1', 'get_ayat(2)'),),
        ),
    ).keyboard

    assert got.to_json() == expected_keyboard.to_json()

import pytest

from apps.bot_init.markup import InlineKeyboard
from apps.bot_init.services.text_message_service import get_keyboard_for_ayat

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayats(mixer):
    return (
        mixer.blend('content.Ayat', ayat=1, sura__number=1),
        mixer.blend('content.Ayat', ayat=1, sura__number=2),
    )


def test(ayats):
    got = get_keyboard_for_ayat(ayats[0])
    expected_keyboard = InlineKeyboard(
        (
            (('Добавить в избранное', f'add_in_favourites({ayats[0].pk})'),),
            (('2:1', f'get_ayat({ayats[1].pk})'),),
        ),
    ).keyboard

    assert got.to_json() == expected_keyboard.to_json()

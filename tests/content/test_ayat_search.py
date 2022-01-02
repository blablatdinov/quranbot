import pytest
from mixer.backend.django import mixer

from apps.bot_init.exceptions import AyatDoesNotExists
from apps.content.services.ayat_search import AyatSearcher

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat():
    mixer.blend('content.Ayat', ayat='1', sura__number=3)
    mixer.blend('content.Ayat', ayat='666', sura__number=8)
    mixer.blend('content.Ayat', ayat='1-5', sura__number=2)
    mixer.blend('content.Ayat', ayat='1, 2', sura__number=114)

    return mixer.blend('content.Ayat', ayat='5', sura__number=4)


@pytest.mark.parametrize('sura_num,ayat_num,expected_ayat_num', [
    (4, 5, '5'),
    (2, 3, '1-5'),
    (8, 666, '666'),
    (114, 2, '1, 2'),
])
def test_logic(ayat, sura_num, ayat_num, expected_ayat_num):
    gotted_ayat = AyatSearcher(sura_num, ayat_num)()

    assert gotted_ayat.ayat == expected_ayat_num
    assert gotted_ayat.sura.number == sura_num


def test_undefined_ayat_searching():
    with pytest.raises(AyatDoesNotExists) as exc:
        queryset = AyatSearcher(sura_number=10, ayat_number='101')()

    assert 'AyatDoesNotExist' in str(exc)

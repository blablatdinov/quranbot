from random import randint

import pytest
from mixer.backend.django import mixer

from apps.api.services.content.content_service import get_ayats_by_sura_number

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayats():
    mixer.cycle(4).blend("content.Ayat", sura__number=1)
    mixer.cycle(5).blend("content.Ayat", sura__number=2)
    mixer.cycle(3).blend("content.Ayat", sura__number=3)
    return 


def test_getting(ayats):
    got = get_ayats_by_sura_number(2)

    assert len(got) == 5

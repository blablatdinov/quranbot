import pytest
from mixer.backend.django import mixer

from apps.content.services.get_unused_ayats import get_unused_ayats

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def morning_contents():
    return mixer.cycle(5).blend('content.MorningContent',)


@pytest.fixture(autouse=True)
def used_ayat(morning_contents):
    for x in morning_contents:
        mixer.blend('content.Ayat', one_day_content=x)


@pytest.fixture(autouse=True)
def unused_ayat():
    mixer.cycle(7).blend('content.Ayat')


def test():
    got = get_unused_ayats()

    assert got.count() == 7

import pytest
from mixer.backend.django import mixer

from apps.bot_init.services.concourse import determine_winners

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def subscribers():
    for _ in range(5):
        referal = mixer.blend('bot_init.Subscriber')
        mixer.cycle(2).blend(
            'bot_init.Subscriber',
            referer=referal,
        )


def test(subscribers):
    got = determine_winners()

    assert len(set(got)) == len(got)

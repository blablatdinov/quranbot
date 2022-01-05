import pytest

from apps.content.exceptions import ContentTooLong
from apps.content.models import Ayat
from apps.content.services.create_morning_content import MorningContentCreator

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def big_ayat(mixer):
    return mixer.blend(
        'content.Ayat',
        content='a' * 5000,
    )


def test(big_ayat):
    with pytest.raises(ContentTooLong):
        MorningContentCreator(1, [big_ayat.pk])()

    assert Ayat.objects.get(pk=big_ayat.pk).one_day_content is None

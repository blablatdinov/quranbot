import pytest

from apps.content.services.get_content_from_morning_content import get_content

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat(mixer):
    return mixer.blend('content.Ayat', ayat='4')


def test_len(ayat):
    additional_content = ''
    got = get_content([ayat], additional_content)
    ayats_len = sum([
        len(ayat.content),
        len(str(ayat.sura.number)),
        len(ayat.ayat),
        len(ayat.sura.link),
        len(additional_content)
    ])

    assert len(got) == ayats_len + 69

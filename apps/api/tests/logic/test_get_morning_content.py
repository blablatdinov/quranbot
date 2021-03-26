import pytest
from mixer.backend.django import mixer

from apps.api.services.content.content_service import get_morning_content

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def morning_content():
    contents = mixer.cycle(20).blend("content.MorningContent")
    return contents


@pytest.fixture()
def ayats(morning_content):
    return mixer.cycle(60).blend("content.Ayat", one_day_content=(x for x in morning_content * 3))


def test_getting(morning_content, ayats):
    got = get_morning_content()

    assert list(got[0].keys()) == ["day", "content"]
    assert type(got) == list
    assert len(got) == 10
    assert "Ссылка на источник:" in got[0].get("content")

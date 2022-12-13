import pytest
import requests_mock

from apps.bot_init.services.text_message_service import get_ayat_by_sura_ayat

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayat(mixer):
    return mixer.blend('content.Ayat', pk=1)


@pytest.fixture()
def quranbot_go_mock():
    with requests_mock.Mocker() as m:
        m.get('http://localhost:8001/content/ayats', json={
            'ayat_id': 1,
        })
        yield m


def test(quranbot_go_mock, ayat):
    got = get_ayat_by_sura_ayat('1:1')

    assert got == ayat

import pytest

from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def nominatim_response():
    with open('tests/prayers/fixtures/nominatium_kazan_search_response.json', 'r') as f:
        return f.read()


@pytest.fixture
def geonames_response():
    with open('tests/prayers/fixtures/geonames_timezone_response.json', 'r') as f:
        return f.read()


@pytest.fixture()
def mock(http_mock, nominatim_response, geonames_response):
    http_mock.get(
        'https://nominatim.openstreetmap.org/search?q=%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C&format=json&limit=1',
        text=nominatim_response,
    )
    http_mock.get(
        'http://api.geonames.org/timezoneJSON?lat=55.7823547&lng=49.1242266&username=blablatdinov',
        text=geonames_response,
    )


@pytest.mark.freeze_time('2021-03-17')
def test_generate_prayers_for_next_day(prayers, subscriber, mock):
    got = PrayerAtUserGenerator(chat_id=subscriber.tg_chat_id, day='tomorrow')()

    assert len(got.prayers) == 6
    assert [p.prayer.name for p in got.prayers] == ['Иртәнге', 'Восход', 'Өйлә', 'Икенде', 'Ахшам', 'Ястү']
    assert str(got.prayers[0].prayer.day.date) == '2021-03-18'

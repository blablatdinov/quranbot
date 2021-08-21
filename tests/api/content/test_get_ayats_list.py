import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def ayats(mixer):
    return mixer.cycle(500).blend('content.Ayat')


def test(client, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        got = client.get('/api/v1/ayats/')
    payload = got.json()
    expected_fields = [
        'id',
        'additional_content',
        'content',
        'arab_text',
        'trans',
        'sura',
        'ayat',
        'link',
        'content_day',
    ]

    assert got.status_code == 200
    assert len(payload['results']) == 50
    assert list(payload['results'][0].keys()) == expected_fields

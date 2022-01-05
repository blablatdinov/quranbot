import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def mailing(mixer):
    return mixer.blend('bot_init.Mailing')


@pytest.fixture(autouse=True)
def mailing_messages(mixer, mailing):
    return mixer.cycle(5).blend('bot_init.Message', mailing=mailing)


def test(client, django_assert_max_num_queries, mailing):
    with django_assert_max_num_queries(3):
        got = client.delete(f'/api/v1/bot/mailings/{mailing.pk}/')

    assert got.status_code == 204

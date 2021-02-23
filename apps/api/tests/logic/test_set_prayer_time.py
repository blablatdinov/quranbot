import pytest

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("is_read", [True, False])
def test_name(client, chat_id, prayer_at_subscriber, is_read):  # FIXME naming
    data = {
        "id": prayer_at_subscriber[0].id,
        "chat_id": chat_id,
        "is_read": is_read,
    }
    got = client.put("/api/v1/setPrayerStatus", data, format="json")

    assert got.status_code == 201
    assert got.json().get("is_read") == is_read

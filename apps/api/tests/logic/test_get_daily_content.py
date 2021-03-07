import pytest

pytestmark = [pytest.mark.django_db]


def test_name(client, daily_content): # FIXME naming
    got = client.get("/api/v1/getDailyContent")
    data = got.json().get("results")

    ######################################## move to serializers test
    data = data.keys()
    ########################################

    assert False, data


"""
apps/api/tests/logic/test_get_daily_content.py::test_name
"""
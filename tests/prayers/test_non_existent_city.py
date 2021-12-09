import pytest
import requests_mock

from apps.prayer.exceptions.city_non_exist import CityNonExist
from apps.prayer.service import get_city_timezone


def test_get_non_existent_city_time_zone():
    with requests_mock.Mocker() as m:
        m.get("https://nominatim.openstreetmap.org/search?q=%D0%9C%D1%83%D1%85%D0%BE%D1%81%D1%80%D0%B0%D0%BD%D1%81%D0%BA&format=json&limit=1", text="[]")
        with pytest.raises(CityNonExist) as exc:
            get_city_timezone("Мухосранскfawioefiwaefjajsdkfj")

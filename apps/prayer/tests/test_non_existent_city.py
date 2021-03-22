import pytest

from apps.prayer.service import get_city_timezone
from apps.prayer.exceptions.city_non_exist import CityNonExist


def test_get_non_existent_city_time_zone():



    with pytest.raises(CityNonExist) as exc:



        get_city_timezone("Мухосранскfawioefiwaefjajsdkfj")

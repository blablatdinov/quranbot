from datetime import datetime
from typing import List

from apps.prayer.models import City, Prayer

SUNRISE_INDEX = 1


class PrayerTimeGetter:
    """Получатель для времени намаза."""
    city: City
    sunrise_time: datetime.time
    prayers: List[Prayer]

    def __init__(self, city_name: str) -> None:
        self.city_name = city_name

    def set_attrs(self) -> None:
        """Установить атрибуты для класса."""
        self.sunrise_time = self.prayers[SUNRISE_INDEX].time
        self.prayers = [
            prayer_time for prayer_time in self.prayers
            if prayer_time.name != 'sunrise'
        ]

    def __call__(self) -> 'PrayerTimeGetter':
        """Entrypoint."""
        self.city = City.objects.filter(name__icontains=self.city_name).first()
        self.prayers = Prayer.objects.filter(city=self.city, day__date=datetime.today())
        self.set_attrs()
        return self

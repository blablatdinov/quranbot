from datetime import datetime

from apps.prayer.models import City, Prayer

SUNRISE_INDEX = 1


class PrayerTimeGetter():
    """Получатель для времени намаза."""

    def __init__(self, city_name) -> None:
        self.city_name = city_name
        pass

    def set_attrs(self):
        """Установить атрибуты для класса."""
        self.city = self.city_name
        self.sunrise_time = self.prayers[SUNRISE_INDEX].time
        self.prayers = [
            prayer_time for prayer_time in self.prayers
            if prayer_time.name != "sunrise"
        ]

    def __call__(self):
        """Entrypoint."""
        self.city = City.objects.filter(name__icontains=self.city_name).first()
        self.prayers = Prayer.objects.filter(city=self.city, day__date=datetime.today())
        self.set_attrs()
        return self

from datetime import datetime, time
import csv
import time as time_
from loguru import logger
from progressbar import progressbar as pbar

import requests

from apps.prayer.models import City, Day, Prayer
from apps.prayer.schemas import PRAYER_NAMES


def get_time_by_str(text: str) -> datetime:
    """Генерируем datetime по строке."""
    return datetime.strptime(text, "%d.%m.%Y")


class PrayerTimeParser():

    def _set_prayers_to_city(self, row):
        day, _ = Day.objects.get_or_create(date=get_time_by_str(row[0]))
        s = [1, 3, 4, 6, 7, 8]
        prayers = []
        for x in range(len(s)):
            prayer_time = time_.strptime(row[s[x]], "%H:%M")
            prayer_time = time(hour=prayer_time.tm_hour, minute=prayer_time.tm_min)
            prayers.append(Prayer(city=self.city, day=day, name=PRAYER_NAMES[x][0], time=prayer_time))
        Prayer.objects.bulk_create(prayers)

    def _get_csv_file(self):
        r = requests.get(self.city.link_to_csv)
        self.csv_file = r.content.decode("utf-8")

    def _parse_prayer_times_for_city(self):
        self._get_csv_file()
        csv_reader = csv.reader(self.csv_file.splitlines(), delimiter=";")
        for row in pbar(csv_reader):
            self._set_prayers_to_city(row)

    def __call__(self):
        logger.info(f"Count of city for parsing: {City.objects.count()}")
        for i, city in enumerate(City.objects.all(), start=1):
            self.city = city
            self._parse_prayer_times_for_city()
            logger.info(f"parsing prayer time for {i}. {city} city")

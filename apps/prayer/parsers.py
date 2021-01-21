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


def prayer_time_parser():
    """Функция парсит данные с сайта http://dum.rt/."""
    logger.info(f"Count of city for parsing: {City.objects.count()}")
    for i, city in enumerate(City.objects.all(), start=1):
        logger.info(f"parsing prayer time for {i}. {city} city")
        r = requests.get(city.link_to_csv)
        decoded_content = r.content.decode("utf-8")
        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=";")
        for row in pbar(csv_reader):
            day, _ = Day.objects.get_or_create(date=datetime.strptime(row[0], "%d.%m.%Y"))
            s = [1, 3, 4, 6, 7, 8]
            prayers = []
            for x in range(len(s)):
                prayer_time = time_.strptime(row[s[x]], "%H:%M")
                prayer_time = time(hour=prayer_time.tm_hour, minute=prayer_time.tm_min)
                prayers.append(Prayer(city=city, day=day, name=PRAYER_NAMES[x][0], time=prayer_time))
            Prayer.objects.bulk_create(prayers)

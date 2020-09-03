import csv
from datetime import datetime, time
import time as time_

import requests

from prayer.models import City, Prayer, Day
from prayer.schemas import PRAYER_NAMES


def get_time_by_str(text: str) -> datetime:
    """Генерируем datetime по строке"""
    return datetime.strptime(text, '%d.%m.%Y')


def prayer_time_parser():
    """Функция парсит данные с сайта http://dum.rt/"""
    for city in City.objects.all():
        r = requests.get(city.link_to_csv)
        decoded_content = r.content.decode('utf-8')
        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=';')
        for row in csv_reader:
            day, _ = Day.objects.get_or_create(date=datetime.strptime(row[0], '%d.%m.%Y'))
            s = [1, 2, 4, 6, 7, 8]
            for x in range(len(s)):
                prayer_time = time_.strptime(row[s[x]], '%H:%M')
                prayer_time = time(hour=prayer_time.tm_hour, minute=prayer_time.tm_min)
                Prayer.objects.get_or_create(city=city, day=day, name=PRAYER_NAMES[x][0], time=prayer_time)

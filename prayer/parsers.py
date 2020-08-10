import csv
from datetime import datetime, time
import time as time_

import requests

from prayer.models import City, Prayer, Day
from prayer.schemas import PRAYER_NAMES


def prayer_time_parser():
    for city in City.objects.all():
        r = requests.get(city.link_to_csv)
        with open('Kazan.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                day = Day.objects.create(date=datetime.strptime(row[0], '%d.%m.%Y'))
                s = [1, 2, 4, 6, 7, 8]
                for x in range(len(s)):
                    a = time_.strptime(row[s[x]], '%H:%M')
                    a = time(hour=a.tm_hour, minute=a.tm_min)
                    Prayer.objects.create(city=city, day=day, name=PRAYER_NAMES[x], time=a)

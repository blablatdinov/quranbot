from datetime import datetime, time
import csv
import time as time_


from loguru import logger
from progressbar import progressbar as pbar
import requests
from bs4 import BeautifulSoup

from apps.prayer.models import City, Day, Prayer
from apps.prayer.schemas import PRAYER_NAMES


def get_time_by_str(text: str) -> datetime:
    """Генерируем datetime по строке."""
    return datetime.strptime(text, "%d.%m.%Y")


class PrayerTimeParser():

    def _set_prayers_to_city(self, row):
        day, _ = Day.objects.get_or_create(date=get_time_by_str(row[0]))
        s = [1, 2, 3, 4, 5, 6]
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

    def _get_row(self, soup):
        result = []
        table = soup.find("table", {"class":"namaz_time"})
        now = datetime.now()  # FIXME может привести к багам из-за часовых поясов
        for row in table.find_all("tr", class_="")[1:]:
            date_and_times = [x.text for x in row.find_all("td")]
            date_and_times[0] = date_and_times[0].split(" ")[0] + f".{now.month}.{now.year}"
            result.append(date_and_times)
        return result

    def _get_page(self):
        url = "https://www.time-namaz.ru/85_ufa_vremy_namaza.html#month_time_namaz"
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        self.city = City.objects.get(name="Ufa")
        date_and_times = self._get_row(soup)
        [self._set_prayers_to_city(x) for x in date_and_times]

    def __call__(self):
        return self._get_page()

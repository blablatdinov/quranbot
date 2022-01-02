import csv
import time as time_
from datetime import datetime, time
from typing import List

import pytz
import requests
from bs4 import BeautifulSoup
from progressbar import progressbar as pbar

from apps.prayer.models import City, Day, Prayer
from apps.prayer.schemas import PRAYER_NAMES


def get_time_by_str(text: str) -> datetime:
    """Генерируем datetime по строке."""
    return datetime.strptime(text, '%d.%m.%Y')


class PrayerTimeParser:
    """Парсер для сайта time-namaz.ru."""

    def __init__(self, city_name: str) -> None:
        self.city_name = city_name
        self.get_city_name_and_urls()

    def __call__(self) -> List[str]:
        """Entrypoint."""
        urls = self.links
        return [self._get_page(url) for url in urls]

    def get_city_name_and_urls(self) -> None:
        """Получить название города и url."""
        self.city_name_in_db = {
            'ufa': 'Уфа',
            'moscow': 'Москва',
        }.get(self.city_name)
        self.links = [
            'https://www.time-namaz.ru/' +
            {
                'ufa': '85_ufa',
                'moscow': '9_moskva',
            }.get(self.city_name) +
            '_vremy_namaza' +
            x for x in ['.html#month_time_namaz', '-next.html#month_time_namaz']
        ]

    def _set_prayers_to_city(self, row: List) -> None:
        date_index = 0
        day, _ = Day.objects.get_or_create(date=get_time_by_str(row[date_index]))
        s = [1, 2, 3, 4, 5, 6]
        prayers = []
        for x in range(len(s)):
            prayer_time = time_.strptime(row[s[x]], '%H:%M')
            prayer_time = time(hour=prayer_time.tm_hour, minute=prayer_time.tm_min)
            if Prayer.objects.filter(day=day, time=prayer_time, city=self.city):
                return
            prayers.append(Prayer(city=self.city, day=day, name=PRAYER_NAMES[x][0], time=prayer_time))
        Prayer.objects.bulk_create(prayers)

    def _get_csv_file(self) -> None:
        r = requests.get(self.city.link_to_csv)
        self.csv_file = r.content.decode('utf-8')

    def _parse_prayer_times_for_city(self) -> None:
        self._get_csv_file()
        csv_reader = csv.reader(self.csv_file.splitlines(), delimiter=';')
        for row in pbar(csv_reader):
            self._set_prayers_to_city(row)

    def _get_row(self, soup: BeautifulSoup) -> List:
        result = []
        table = soup.find('table', class_='namaz_time')
        for index, row in enumerate(table.find_all('tr', class_='')):
            if index == 0:
                month = self.get_month_number(row.find('th').text)
                continue
            date_and_times = [x.text for x in row.find_all('td')]
            date_and_times[0] = (
                date_and_times[0].split(' ')[0] +
                f'.{month}.{datetime.now(tz=pytz.timezone("Europe/Zurich")).year}'
            )
            result.append(date_and_times)
        return result

    @staticmethod
    def get_month_number(month_name: str) -> int:
        """Получить номер месяца по имени."""
        return {
            'Январь': 1,
            'Февраль': 2,
            'Март': 3,
            'Апрель': 4,
            'Май': 5,
            'Июнь': 6,
            'Июль': 7,
            'Август': 8,
            'Сентябрь': 9,
            'Октябрь': 10,
            'Ноябрь': 11,
            'Декабрь': 12,
        }.get(month_name)

    def _get_page(self, url: str) -> None:
        response = requests.get(
            url,
            headers={
                'Host': 'www.time-namaz.ru',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv86.0) Gecko/20100101 Firefox/86.0',
                'Accept': 'image/webp,*/*',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.time-namaz.ru/85_ufa_vremy_namaza.html',
                'Cookie': (
                    'user_siti=%D0%A3%D1%84%D0%B0; _ym_uid=1616427869978783309;'
                    '_ym_d=1616427869; _ga=GA1.2.196004999.1616427871;'
                    '_gid=GA1.2.1839317671.1616427871; PHPSESSID=a9b692157fc71f8acfad25037a16c62a; _ym_isad=1;'
                    '_gat_gtag_UA_158129949_1=1'
                ),
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'TE': 'Trailers',
            },
        ).text
        soup = BeautifulSoup(response, 'lxml')
        self.city = City.objects.get(name=self.city_name_in_db)
        date_and_times = self._get_row(soup)
        [self._set_prayers_to_city(x) for x in date_and_times]

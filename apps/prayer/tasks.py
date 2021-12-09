from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from celery.task import periodic_task

from apps.prayer.parsers.time_namaz_ru_parser import PrayerTimeParser
from apps.prayer.service import send_prayer_time


@periodic_task(run_every=(crontab(hour=20, minute=00)), name="send_prayer_times (20:00)")
def daily_prayer_time_sender():
    """Таска для рассылки времени намазов."""
    send_prayer_time()


@periodic_task(run_every=(crontab(day_of_week=2, hour=6, minute=00)), name="parse prayer times")
def parse_prayer_times():
    """Спарсить времена намазов."""
    for city_name in ["moscow", "ufa"]:
        PrayerTimeParser(city_name=city_name)()

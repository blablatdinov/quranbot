from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from celery.task import periodic_task

from apps.content.podcast_parser import PodcastParser
from apps.content.service import do_morning_content_distribution


@periodic_task(run_every=(crontab(hour=7, minute=0)), name='mailing (7:00)')
def mailing() -> None:
    """Таска для рассылки ежедневного контента."""
    do_morning_content_distribution()


@periodic_task(run_every=(crontab(day_of_week=1, hour=5)), name='parse new podcasts (Monday)')
def parse_new_podcasts() -> None:
    """Скачать подкасты, вышедшие за неделю."""
    PodcastParser()()

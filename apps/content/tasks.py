from __future__ import absolute_import, unicode_literals
from apps.content.podcast_parser import PodcastParser

from celery.schedules import crontab
from celery.task import periodic_task

from apps.content.service import do_morning_content_distribution


@periodic_task(run_every=(crontab(hour=7, minute=0)), name="mailing (7:00)")
def mailing():
    """Таска для рассылки ежедневного контента."""
    do_morning_content_distribution()


@periodic_task(run_every=(crontab(day_of_week=1, hour=5)), name="parse new podcasts (Monday)")
def parse_new_podcasts():
    PodcastParser()()

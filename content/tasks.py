from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from content.service import do_morning_content_distribution


@periodic_task(run_every=(crontab(hour=7, minute=0)), name='mailing')
def mailing():
    do_morning_content_distribution()

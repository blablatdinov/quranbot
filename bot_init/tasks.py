from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from content.service import do_morning_content_distribution
from bot_init import upload_database_dump


@periodic_task(run_every=(crontab(hour=7, minute=30)), name='mailing')
def mailing():
    upload_database_dump()

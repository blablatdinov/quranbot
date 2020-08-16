from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from content.service import do_morning_content_distribution
from bot_init.service import upload_database_dump, count_active_users


@periodic_task(run_every=(crontab(hour=7, minute=30)), name='upload_dump')
def upload_dump():
    upload_database_dump()


@periodic_task(run_every=(crontab(hour=6, minute=30)), name='check_users')
def check_users():
    count_active_users()

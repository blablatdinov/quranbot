from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta
from .views import tbot

# celery worker -A quranbot --loglevel=info
# celery -A quranbot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
@periodic_task(run_every=timedelta(seconds=5), name='mft')
# @shared_task
def mft():
    tbot.send_message(chat_id=358610865, text='celery')
    print('celery')


@shared_task
def add(x, y):
    return x + y

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from content.service import do_morning_content_distribution
from prayer.service import send_prayer_time


@periodic_task(run_every=(crontab(hour=20, minute=00)), name='send_prayer_times')
def mailing():
    send_prayer_time()

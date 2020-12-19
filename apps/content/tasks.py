from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from celery.task import periodic_task

from apps.content.service import do_morning_content_distribution


@periodic_task(run_every=(crontab(hour=7, minute=0)), name="mailing")
def mailing():
    """Таска для рассылки ежедневного контента."""
    do_morning_content_distribution()

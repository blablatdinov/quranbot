from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.task import periodic_task

from apps.bot_init.service import count_active_users, upload_database_dump


@periodic_task(run_every=(crontab(hour=7, minute=30)), name="upload_dump (7:30)")
def upload_dump():
    """Таска для выгрузки дампа."""
    upload_database_dump()


@periodic_task(run_every=(crontab(hour=6, minute=30)), name="check_users (6:30)")
def check_users():
    """Таска для проверки кол-ва активных пользователей."""
    count_active_users()

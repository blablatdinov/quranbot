from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.task import periodic_task

from bot_init.service import count_active_users, upload_database_dump


@periodic_task(run_every=(crontab(hour=7, minute=30)), name="upload_dump")
def upload_dump():
    """Таска для выгрузки дампа."""
    upload_database_dump()


@periodic_task(run_every=(crontab(hour=6, minute=30)), name="check_users")
def check_users():
    """Таска для проверки кол-ва активных пользователей."""
    count_active_users()

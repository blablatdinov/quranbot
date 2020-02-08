from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.task import periodic_task
from .models import Subscribers, QuranOneDayContent
from celery.schedules import crontab
from datetime import timedelta
from .views import tbot


# celery worker -A quranbot --loglevel=info
# celery -A quranbot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
@periodic_task(run_every=timedelta(seconds=5), name='mailing')
# @shared_task
def mailing():
    subs = Subscribers.objects.filter(status=True)  # Получаем подписчиков
    for sub in subs:  # Проходимся по подписчикам
        content = QuranOneDayContent.objects.filter(day=sub.day)  # Получаем контент для подписчика
        try:
            tbot.send_message(chat_id=sub.telegram_chat_id, text=content)
            sub.day += 1
            sub.save()
        except:
            sub.status = False
            sub.save()


@shared_task
def add(x, y):
    return x + y

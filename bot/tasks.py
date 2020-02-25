from __future__ import absolute_import, unicode_literals
from celery import shared_task
from telebot.apihelper import ApiException

from celery.task import periodic_task
from .models import Subscribers, QuranOneDayContent, QuranAyat
from celery.schedules import crontab
from datetime import timedelta
from .views import tbot


# celery worker -A quranbot --loglevel=info
# celery -A quranbot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#@periodic_task(run_every=(timedelta(seconds=5)), name='mailing')
@periodic_task(run_every=(crontab(hour=8, minute=28)), name='mailing')
#@periodic_task(name='mailing')
def mailing():
    subs = Subscribers.objects.filter(status=True)  # Получаем подписчиков
    print(subs)
    for sub in subs:  # Проходимся по подписчикам
        print(sub)
        content = QuranOneDayContent.objects.get(day=sub.day).content_for_day()
        try:
            tbot.send_message(chat_id=sub.telegram_chat_id, text=content, parse_mode='Markdown')
            sub.day += 1
            sub.save()
        except ApiException:
            sub.status = False
            sub.save()


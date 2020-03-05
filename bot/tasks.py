from __future__ import absolute_import, unicode_literals
from celery import shared_task
from telebot.apihelper import ApiException

from celery.task import periodic_task
from .models import Subscribers, QuranOneDayContent, QuranAyat
from celery.schedules import crontab
from datetime import timedelta
from .views import tbot
from .utils import save_message

import lxml
from bs4 import BeautifulSoup as bs
import requests
import time



# celery worker -A quranbot --loglevel=info
# celery -A quranbot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#@periodic_task(run_every=(timedelta(seconds=5)), name='mailing')
@periodic_task(run_every=(crontab(hour=4, minute=0)), name='mailing')
#@periodic_task(name='mailing')
def mailing():
    subs = Subscribers.objects.filter(status=True)  # Получаем подписчиков
    print(subs)
    for sub in subs:  # Проходимся по подписчикам
        print(sub)
        content = QuranOneDayContent.objects.get(day=sub.day).content_for_day()
        try:
            msg = tbot.send_message(chat_id=sub.telegram_chat_id, text=content, parse_mode='Markdown')
            save_message(msg)
            sub.day += 1
            sub.save()
        except ApiException:
            sub.status = False
            sub.save()
        time.sleep(0.1)


@periodic_task(run_every=(crontab(hour=3, minute=0)), name='prayer-time')
def pr_time():
    sub = Subscribers.objects.get(pk=1)
    soup = bs(requests.get('https://umma.ru/raspisanie-namaza/kazan').text, 'lxml')
    block = soup.find('tr', class_='current')
    columns = block.find_all('td')
    res = f"Иртәнге: {columns[2].text}\n"\
    f"Восход: {columns[3].text}\n"\
    f"Өйлә: {columns[4].text}\n" \
    f"Икенде: {columns[5].text}\n" \
    f"Ахшам: {columns[6].text}\n" \
    f"Ястү: {columns[7].text}"
    msg = tbot.send_message(sub, res)
    save_message(msg)




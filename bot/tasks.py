from __future__ import absolute_import, unicode_literals
from celery import shared_task
from telebot.apihelper import ApiException

from celery.task import periodic_task
from .models import Subscribers, QuranOneDayContent, QuranAyat, Audio
from celery.schedules import crontab
from datetime import timedelta
from .views import tbot
from .utils import save_message

import lxml
from bs4 import BeautifulSoup as bs
import requests
import time



@periodic_task(run_every=(crontab(hour=4, minute=0)), name='mailing')
def mailing():
    subs = Subscribers.objects.filter(status=True)  # Получаем подписчиков
    for sub in subs:  # Проходимся по подписчикам
        content = QuranOneDayContent.objects.get(day=sub.day).content_for_day()
        try:
            msg = tbot.send_message(chat_id=sub.telegram_chat_id, text=content, parse_mode='HTML')
            save_message(msg)
            sub.day += 1
            sub.save()
            time.sleep(0.1)
        except ApiException:
            sub.status = False
            sub.save()
            msg = tbot.send_message(chat_id=358610865, text=f'Пользователь {sub.telegram_chat_id} отписан')
            save_message(msg)


@periodic_task(run_every=(crontab(hour=3, minute=0)), name='prayer-time')
def pr_time():
    sub = Subscribers.objects.get(telegram_chat_id=358610865)
    soup = bs(requests.get('https://umma.ru/raspisanie-namaza/kazan').text, 'lxml')
    block = soup.find('tr', class_='current')
    columns = block.find_all('td')
    n_for_columns = 1
    res = f"Иртәнге: {columns[n_for_columns + 1].text}\n"\
    f"Восход: {columns[n_for_columns + 2].text}\n"\
    f"Өйлә: {columns[n_for_columns + 3].text}\n" \
    f"Икенде: {columns[n_for_columns + 4].text}\n" \
    f"Ахшам: {columns[n_for_columns + 5].text}\n" \
    f"Ястү: {columns[n_for_columns + 6].text}"
    msg = tbot.send_message(sub, res)
    save_message(msg)


#@periodic_task()
def parse_audio():
    urls = ['https://umma.ru/audlo/shamil-alyautdinov/']
    last_audio_in_db = Audio.objects.last().title
    count = 0
    main_while_break_flag = False

    while True:
        soup = bs(requests.get(urls[count]).text, 'lxml')
        articles = soup.find_all('article')
        print(len(articles))
        for article in articles:
            if article.find('h2').text == last_audio_in_db:
                main_while_break_flag = True
                break
            print(article.text)
            article_link = 'https://umma.ru' + article.find('a')['href']
            article_soup = bs(requests.get(article_link).text, 'lxml')
            print(article_soup)
            audio_download_link = article_soup.find('a', class_='download-audio')['href']
        exit()


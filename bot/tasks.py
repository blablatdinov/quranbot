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
import logging


log = logging.getLogger(__name__)



@periodic_task(run_every=(crontab(hour=7, minute=0)), name='mailing')
def mailing():
    order_to_admin = ''
    subs = Subscribers.objects.filter(status=True)
    try:
        for sub in subs:
            content = QuranOneDayContent.objects.get(day=sub.day).content_for_day()
            msg = tbot.send_message(chat_id=sub.telegram_chat_id, text=content, parse_mode='HTML')
            save_message(msg)
            sub.day += 1
            sub.save()
            time.sleep(0.1)
    except ApiException as e:
        if 'bot was blocked by the user' in str(e):
            sub.status = False
            sub.save()
            order_to_admin += f'Пользователь {sub.telegram_chat_id} отписан\n'
            #msg = tbot.send_message(chat_id=358610865, text=f'Пользователь {sub.telegram_chat_id} отписан')
        else:
            msg = tbot.send_message(chat_id=358610865, text=f'Непредвиденная ошибка')
            log.error(str(e))
        save_message(msg)
    except QuranOneDayContent.DoesNotExist:
        order_to_admin += f'Закончился ежедневный контент\n'
    order_to_admin += f'Осталось контента на {subs.order_by("day").last().day - QuranOneDayContent.objects.all().order_by("day").last().day - 1} дней'
    msg = tbot.send_message(chat_id=358610865, text=order_to_admin)
    save_message(msg)



@periodic_task(run_every=(crontab(hour=6, minute=0)), name='prayer-time')
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


@periodic_task(run_every=(crontab(hour=20, minute=0, day_of_week=6)), name='audio_parser')
def audio_parser():
    from bot.models import Audio
    import sys
    counter = 1
    pag_pages = ['https://umma.ru/audlo/shamil-alyautdinov/']
    sub = Subscribers.objects.get(comment='Я')
    last_audio_in_db_link = Audio.objects.filter(is_flag=True).reverse()[0].audio_link
    #last_audio_in_db_link = 'https://umma.ru/uploads/audio/ous97eldud.mp3'
    print(last_audio_in_db_link)
    breakFlag = False
    while True:
        soup = bs(requests.get(pag_pages[-1]).text, 'lxml')
        article_blocks = soup.find_all('article')
        for block in article_blocks:
            link = 'https://umma.ru' + block.find('div', class_='main').find('a')['href']
            soup = bs(requests.get(link).text, 'lxml')
            audio_link = soup.find('audio').find('a')['href']
            title = soup.find('h1').text.strip()
            print(audio_link)
            if audio_link == last_audio_in_db_link:
                breakFlag = True
                break
            else:
                print(title)
                r = requests.get(audio_link)
                print(r)
                if sys.getsizeof(r.content) < 50 * 1024 * 1024:
                    continue
                    print('upload to telegram')
                    msg = tbot.send_audio(sub.telegram_chat_id, r.content, timeout=180,
                                          title=title, performer='Шамиль Аляутдинов')
                    save_message(msg)
                    print('add to db')
                    Audio.objects.create(title=title, audio_link=audio_link,
                                         tg_audio_link=msg.audio.file_id)
                    #tbot.delete_message(sub.telegram_chat_id, msg.message_id)
                else:
                    Audio.objects.create(title=title, audio_link=audio_link)
        if breakFlag:
            break

        # Генерируем ссылки для следующей итерации while
        counter += 1
        pag_pages.append(f'https://umma.ru/audlo/shamil-alyautdinov/page/{counter}')

import csv
from datetime import datetime

from django.db.models import QuerySet

from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber
from bot_init.schemas import Answer
from bot_init.service import send_answer
from prayer.models import PrayerAtUser, PrayerAtUserGroup, City, Prayer


def get_prayer_time(city: City):
    p = Prayer.objects.filter(city=city, day__date=datetime.today())
    return p


def get_emoji_for_button(prayer: PrayerAtUser):
    return '❌' if not prayer.is_read else '✅'


def get_buttons(subscriber: Subscriber = None, prayer_times: QuerySet = None, prayer_pk: int = None):
    if prayer_pk is None:
        prayer_group = PrayerAtUserGroup.objects.create()
        prayers = [PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
                   for prayer in prayer_times]
    else:
        prayer = PrayerAtUser.objects.get(pk=prayer_pk)
        prayers = PrayerAtUser.objects.filter(prayer_group=prayer.prayer_group)
    buttons = [
        [(get_emoji_for_button(x), f'change_prayer_status({x.pk})') for x in prayers]
    ]
    return buttons


def send_prayer_time():
    for subscriber in Subscriber.objects.filter(city__isnull=False):
        prayer_times = get_prayer_time(subscriber.city)
        text = f'Время намаза для г. Казань ({datetime.today().strftime("%d.%m.%Y")}) \n\n' \
               f'Утренний: {prayer_times[0].time.strftime("%H:%M")}\n' \
               f'Восход: {prayer_times[1].time.strftime("%H:%M")}\n' \
               f'Обеденный: {prayer_times[2].time.strftime("%H:%M")}\n' \
               f'Послеобеденный: {prayer_times[3].time.strftime("%H:%M")}\n' \
               f'Вечерный: {prayer_times[4].time.strftime("%H:%M")}\n' \
               f'Ночной: {prayer_times[5].time.strftime("%H:%M")}\n'
        buttons = get_buttons(subscriber, prayer_times.exclude(name='sunrise'))
        keyboard = InlineKeyboard(buttons).keyboard
        send_answer(Answer(text, keyboard=keyboard), subscriber.tg_chat_id)

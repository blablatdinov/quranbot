import csv
from datetime import datetime

from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber
from bot_init.schemas import Answer
from bot_init.service import send_answer
from prayer.models import Prayer, PrayerGroup


def get_prayer_time():
    with open('Kazan.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            if datetime.now().strftime('%d.%m.%Y') == row[0]:
                return row


def get_emoji_for_button(prayer: Prayer):
    return '❌' if not prayer.is_read else '✅'


def get_buttons(subscriber: Subscriber = None, prayer_pk: int = None):
    if prayer_pk is None:
        prayer_group = PrayerGroup.objects.create()
        prayers = [Prayer.objects.create(subscriber=subscriber, prayer_group=prayer_group) for _ in range(5)]
    else:
        prayer = Prayer.objects.get(pk=prayer_pk)
        prayers = Prayer.objects.filter(prayer_group=prayer.prayer_group)
    buttons = [
        [(get_emoji_for_button(x), f'change_prayer_status({x.pk})') for x in prayers]
    ]
    return buttons


def send_prayer_time():
    for subscriber in Subscriber.objects.all():
        prayer_times = get_prayer_time()
        text = f'Время намаза для г. Казань ({prayer_times[0]}) \n\n' \
               f'Утренний: {prayer_times[1]}\n' \
               f'Восход: {prayer_times[2]}\n' \
               f'Обеденный: {prayer_times[4]}\n' \
               f'Послеобеденный: {prayer_times[6]}\n' \
               f'Вечерный: {prayer_times[7]}\n' \
               f'Ночной: {prayer_times[8]}\n'
        buttons = get_buttons(subscriber)
        keyboard = InlineKeyboard(buttons).keyboard
        send_answer(Answer(text, keyboard=keyboard), subscriber.tg_chat_id)

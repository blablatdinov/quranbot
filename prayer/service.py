import csv
from datetime import datetime
from datetime import timedelta

from django.db.models import QuerySet
from geopy.geocoders import Nominatim
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber
from bot_init.schemas import Answer
from bot_init.service import send_answer
from prayer.models import PrayerAtUser, PrayerAtUserGroup, City, Prayer
from prayer.schemas import PRAYER_NAMES


def get_address(x, y):
    geolocator = Nominatim(user_agent="qbot")
    location = geolocator.reverse(f"{x}, {y}")
    return location.address


def set_city_to_subscriber_by_location(location: tuple, chat_id: int):  # TODO создать ф-ю для доставания подписчика с try, except
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    address = get_address(location[0], location[1])
    address_split = address.replace(', ', ' ').split(' ')
    for elem in address_split:
        if city := City.objects.filter(name__contains=elem).first():
            subscriber.city = city
            subscriber.save(update_fields=['city'])
            return Answer(f'Вам будет приходить время намаза для г. {city.name}')
    print(location, address)  # TODO логгировать
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Поиск города", switch_inline_query_current_chat='')
    keyboard.add(button)
    return Answer('Город не найден', keyboard=keyboard)


def get_prayer_time(city: City):
    """Возвращает время намазов для следующего дня"""
    date = datetime.today() + timedelta(days=1)
    p = Prayer.objects.filter(city=city, day__date=date)
    return p


def get_emoji_for_button(prayer: PrayerAtUser):
    """Возвращает эмоджи для кнопки в зависимости от того, прочитан намаз или нет"""
    return '❌' if not prayer.is_read else '✅'


def get_buttons(subscriber: Subscriber = None, prayer_times: QuerySet = None, prayer_pk: int = None):
    """Возвращает кнопки со статусом намазов"""
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
    """Рассылаем время намаза с кнопками"""
    for subscriber in Subscriber.objects.filter(city__isnull=False):
        prayer_times = get_prayer_time(subscriber.city)
        text = f'Время намаза для г. Казань ({(datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")}) \n\n' \
               f'Утренний: {prayer_times[0].time.strftime("%H:%M")}\n' \
               f'Восход: {prayer_times[1].time.strftime("%H:%M")}\n' \
               f'Обеденный: {prayer_times[2].time.strftime("%H:%M")}\n' \
               f'Послеобеденный: {prayer_times[3].time.strftime("%H:%M")}\n' \
               f'Вечерный: {prayer_times[4].time.strftime("%H:%M")}\n' \
               f'Ночной: {prayer_times[5].time.strftime("%H:%M")}\n'
        buttons = get_buttons(subscriber, prayer_times.exclude(name='sunrise'))
        keyboard = InlineKeyboard(buttons).keyboard
        send_answer(Answer(text, keyboard=keyboard), subscriber.tg_chat_id)


def get_keyboard_for_unread_prayers(prayers: QuerySet, chat_id: int):
    buttons = []
    for i in [0, 2, 3, 4, 5]:
        prayer_name = PRAYER_NAMES[i][1]
        buttons.append(((f'{prayer_name} - 1', f'unread_prayer_type_minus_one({prayer_name}, {chat_id})'),),)
    return InlineKeyboard(buttons).keyboard



def get_unread_prayers(chat_id):
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    unread_prayers = PrayerAtUser.objects.filter(subscriber=subscriber, is_read=False)
    text = 'Непрочитано\n\n'
    for i in [0, 2, 3, 4, 5]:
        prayer_type_group = unread_prayers.filter(prayer__name=PRAYER_NAMES[i][0])
        text += f'{PRAYER_NAMES[i][1]}: {prayer_type_group.count()}\n'
    return Answer(text, keyboard=get_keyboard_for_unread_prayers(unread_prayers, chat_id))

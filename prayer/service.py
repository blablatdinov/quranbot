from datetime import datetime
from datetime import timedelta
from typing import List, Tuple

from django.db.models import QuerySet
from geopy.geocoders import Nominatim
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber, Mailing
from bot_init.schemas import Answer
from bot_init.service import send_answer, get_subscriber_by_chat_id
from prayer.models import PrayerAtUser, PrayerAtUserGroup, City, Prayer
from prayer.schemas import PRAYER_NAMES


def get_address(x: str, y: str):
    """Получаем аддресс по координатам благодаря библиотеке geopy"""
    geolocator = Nominatim(user_agent="qbot")
    location = geolocator.reverse(f"{x}, {y}")
    return location.address


def set_city_to_subscriber(city: City, chat_id: int) -> Answer:
    subscriber = get_subscriber_by_chat_id(chat_id)
    subscriber.city = city
    subscriber.save(update_fields=['city'])
    return Answer(f'Вам будет приходить время намаза для г. {city.name}')


def get_city_not_found_answer(text: str = None) -> Answer:
    if text is None:
        text = 'Город не найден,\nвоспользуйтесь поиском'
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Поиск города", switch_inline_query_current_chat='')
    keyboard.add(button)
    return Answer(text, keyboard=keyboard)


def set_city_to_subscriber_by_location(location: tuple, chat_id: int) -> Answer:
    """Ищем город и если не находим, то предлагаем пользователю найти в поиске"""
    # TODO создать ф-ю для доставания подписчика с try, except. Побить функцию
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    address = get_address(location[0], location[1])

    address_split = address.replace(', ', ' ').split(' ')
    for elem in address_split:
        if city := City.objects.filter(name__contains=elem).first():
            answer = set_city_to_subscriber(city, subscriber.tg_chat_id)
            return answer
    print(location, address)  # TODO логгировать
    return get_city_not_found_answer()


def get_prayer_time(city: City, date: datetime = datetime.today() + timedelta(days=1)) -> QuerySet:
    """Возвращает время намазов для следующего дня"""
    prayers = Prayer.objects.filter(city=city, day__date=date)
    return prayers


def get_emoji_for_button(prayer: PrayerAtUser) -> str:
    """Возвращает эмоджи для кнопки в зависимости от того, прочитан намаз или нет"""
    return '❌' if not prayer.is_read else '✅'


def get_buttons(
        subscriber: Subscriber = None,
        prayer_times: QuerySet = None,
        prayer_pk: int = None) -> List[List[Tuple[str, str]]]:
    """Возвращает кнопки со статусом намазов"""
    if prayer_pk is None:
        prayer_group = PrayerAtUserGroup.objects.create()
        prayers = [PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
                   for prayer in prayer_times]
    else:
        prayer = PrayerAtUser.objects.get(pk=prayer_pk)
        prayers = PrayerAtUser.objects.filter(prayer_group=prayer.prayer_group).order_by('pk')
    buttons = [
        [(get_emoji_for_button(x), f'change_prayer_status({x.pk})') for x in prayers]
    ]
    return buttons


def get_text_prayer_times(prayer_times: QuerySet, city_name: str, date: datetime) -> str:
    res = f'Время намаза для г. {city_name} ({date.strftime("%d.%m.%Y")}) \n\n'
    for i in range(6):
        res += f'{prayer_times[i].get_name_display()}: {prayer_times[i].time.strftime("%H:%M")}\n'
    return res


def send_prayer_time(date: datetime = None) -> None:  # TODO одинаковы куски кода content.service.do_morning_content_distribution
    """Рассылаем время намаза с кнопками"""
    if date is None:
        date = (datetime.today() + timedelta(days=1))
    mailing = Mailing.objects.create()
    for subscriber in Subscriber.objects.filter(city__isnull=False):
        prayer_times = get_prayer_time(subscriber.city, date)
        text = get_text_prayer_times(prayer_times, subscriber.city.name, date)
        message_instance = send_answer(Answer(text), subscriber.tg_chat_id)

        message_instance.mailing = mailing
        message_instance.save(update_fields=['mailing'])
    text = f'Рассылка #{mailing.pk} завершена'
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=['mailing'])


def get_unread_prayers_by_chat_id(chat_id: int) -> QuerySet:
    """Получаем непрочитанные намазы у подписчика"""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    unread_prayers = PrayerAtUser.objects.filter(subscriber=subscriber, is_read=False)
    return unread_prayers


def unread_prayer_type_minus_one(chat_id: int, prayer_type_id: int) -> None:
    """Уменьшаем кол-во непрочитанных намазов отдельной категории на один"""
    unread_prayers = get_unread_prayers_by_chat_id(chat_id)
    prayer_name = PRAYER_NAMES[prayer_type_id][0]
    separate_unread_prayer = unread_prayers.filter(prayer__name=prayer_name).first()
    separate_unread_prayer.is_read = True
    separate_unread_prayer.save(update_fields=['is_read'])


def get_keyboard_for_unread_prayers(chat_id: int) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для непрочитанных намазаов. Чтобы люди при нажатии могли уменьшать их кол-во"""
    buttons = []
    for prayer_type_id in [0, 2, 3, 4, 5]:
        prayer_name = PRAYER_NAMES[prayer_type_id][1]
        buttons.append(((f'{prayer_name} - 1', f'unread_prayer_type_minus_one({prayer_type_id}, {chat_id})'),),)
    return InlineKeyboard(buttons).keyboard


def get_unread_prayers(chat_id) -> Answer:
    """Возвращает кол-во непрочитанных намазов с клавиатурой"""
    text = 'Непрочитано\n\n'
    unread_prayers = get_unread_prayers_by_chat_id(chat_id)
    for i in [0, 2, 3, 4, 5]:
        prayer_type_group = unread_prayers.filter(prayer__name=PRAYER_NAMES[i][0])
        text += f'{PRAYER_NAMES[i][1]}: {prayer_type_group.count()}\n'
    return Answer(text, keyboard=get_keyboard_for_unread_prayers(chat_id))


def get_prayer_time_or_no(chat_id: int) -> Answer:
    subscriber = get_subscriber_by_chat_id(chat_id)
    if subscriber.city is None:
        return get_city_not_found_answer(text='Вы не указали город, отправьте местоположение или воспользуйтесь поиском')
    today = datetime.now()
    prayers = get_prayer_time(subscriber.city, today)
    text = get_text_prayer_times(prayers, subscriber.city.name, today)
    answer = Answer(text)
    return answer


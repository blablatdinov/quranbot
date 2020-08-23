from datetime import datetime, timedelta, time
from typing import List, Tuple

from django.db.models import QuerySet, Q
from geopy.geocoders import Nominatim
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_init.markup import InlineKeyboard
from bot_init.models import Subscriber, Mailing
from bot_init.schemas import Answer
from bot_init.service import send_answer, get_subscriber_by_chat_id, send_message_to_admin
from prayer.models import PrayerAtUser, PrayerAtUserGroup, City, Prayer, Day
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


def generate_prayer_at_user(chat_id: int, prayers: QuerySet):
    """Функция должна генерировать новы PrayerAtUser или возвращать те, которые уже есть"""
    # TODO подумать над названием (сгенерировать или вернуть то, что есть)
    # TODO сделать тест на разные дни
    subscriber = get_subscriber_by_chat_id(chat_id)
    # Найти те, которые уже есть
    if PrayerAtUser.objects.filter(subscriber=subscriber, prayer__day=prayers[0].day):
        query = Q()
        for prayer in prayers:
            query = query | Q(prayer=prayer)
        prayers_at_user = PrayerAtUser.objects.filter(subscriber=subscriber).filter(query)
        return list(prayers_at_user)
    # Генерировать
    prayer_group = PrayerAtUserGroup.objects.create()
    result = [
        PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
        for prayer in prayers.exclude(name='sunrise')
    ]
    return result


def get_emoji_for_button(prayer: PrayerAtUser) -> str:
    """Возвращает эмоджи для кнопки в зависимости от того, прочитан намаз или нет"""
    return '❌' if not prayer.is_read else '✅'


def get_buttons(  # FIXME если пользователь запрашивает время намаза два раза, ему каздый раз генерируется PrayerAtUser
        subscriber: Subscriber = None,
        prayer_times: QuerySet = None,
        prayer_at_user_pk: int = None) -> List[List[Tuple[str, str]]]:
    """Возвращает кнопки со статусом намазов"""
    # TODO если пользователь получил 2 времени намаза в разных городах в один день, вероятно будет ошибка

    # TODO добавить сортировку

    text_for_read_prayer = 'set_prayer_status_to_unread({})'
    text_for_unread_prayer = 'set_prayer_status_to_read({})'
    if prayer_at_user_pk:
        day = PrayerAtUser.objects.get(pk=prayer_at_user_pk).prayer.day
        prayers = PrayerAtUser.objects.filter(prayer__day=day).order_by('pk')
    else:
        prayers = generate_prayer_at_user(subscriber.tg_chat_id, prayer_times.order_by('pk'))
    buttons = []
    for x in prayers:
        handle_text = text_for_read_prayer.format(x.pk) if x.is_read else text_for_unread_prayer.format(x.pk)
        buttons.append(
            (get_emoji_for_button(x) + str(x.pk), handle_text),
        )
    from pprint import pprint
    pprint(buttons)
    return [buttons]


def get_text_prayer_times(prayer_times: QuerySet, city_name: str, date: datetime) -> str:
    res = f'Время намаза для г. {city_name} ({date.strftime("%d.%m.%Y")}) \n\n'
    for i in range(6):
        prayer = prayer_times[i]
        res += f'{prayer.pk} {prayer.get_name_display()}: {prayer.time.strftime("%H:%M")} {prayer.day}\n'
    return res


def send_prayer_time(date: datetime = None) -> None:  # TODO одинаковы куски кода content.service.do_morning_content_distribution
    """Рассылаем время намаза с кнопками"""
    # TODO написать тесты
    if date is None:
        date = (datetime.today() + timedelta(days=1))
    mailing = Mailing.objects.create()
    for subscriber in Subscriber.objects.filter(city__isnull=False):
        prayer_times = get_prayer_time(subscriber.city, date)
        text = get_text_prayer_times(prayer_times, subscriber.city.name, date)
        keyboard = InlineKeyboard(get_buttons(subscriber, prayer_times.exclude(name='sunrise'))).keyboard
        message_instance = send_answer(Answer(text, keyboard=keyboard), subscriber.tg_chat_id)

        message_instance.mailing = mailing
        message_instance.save(update_fields=['mailing'])
    text = f'Рассылка #{mailing.pk} завершена'
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=['mailing'])


def get_now_prayer(chat_id: int, date_time=None):
    date_time = date_time if date_time is not None else datetime.now()
    prayer_time = time(hour=date_time.hour, minute=date_time.minute)
    prayer = Prayer.objects.filter(
        day__date=date_time,
        city__subscriber__tg_chat_id=chat_id,
        time__lt=prayer_time
    ).last()
    return prayer


def get_unread_prayers_by_chat_id(chat_id: int, date_time: datetime = None) -> QuerySet:
    """Получаем непрочитанные намазы у подписчика"""
    date_time = date_time if date_time is not None else datetime.now()
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    now_prayer = get_now_prayer(chat_id, date_time)
    unread_prayers = PrayerAtUser.objects.filter(
        subscriber=subscriber,
        is_read=False,
        prayer__day__date__lte=date_time,  # меньше или равно
        prayer__time__lt=date_time.time()
    ).order_by('-pk')[1:]
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
    keyboard = InlineKeyboard(get_buttons(subscriber, prayers)).keyboard
    answer = Answer(text, keyboard=keyboard)
    return answer


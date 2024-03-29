"""Бизнес логика для намазов."""
from datetime import datetime, time, timedelta
from typing import List, Tuple, Union

from django.conf import settings
from django.db.models import Q, QuerySet
from loguru import logger
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.bot_init.markup import InlineKeyboard
from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.service import get_subscriber_by_chat_id, send_message_to_admin
from apps.bot_init.services.answer_service import Answer
from apps.prayer.models import City, Prayer, PrayerAtUser, PrayerAtUserGroup
from apps.prayer.schemas import PRAYER_NAMES


def get_city_not_found_answer(text: str = None) -> Answer:
    """Генерирует ответ если подписчик с неустановленным городом пытается получить время намаза."""
    if text is None:
        text = 'Город не найден,\nвоспользуйтесь поиском'
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Поиск города', switch_inline_query_current_chat='')
    keyboard.add(button)
    return Answer(text, keyboard=keyboard)


def get_prayer_time(city: City, date: datetime = datetime.today() + timedelta(days=1)) -> QuerySet:
    """Возвращает время намазов для следующего дня."""
    prayers = Prayer.objects.filter(city=city, day__date=date).order_by('pk')
    return prayers


def generate_prayer_at_user(chat_id: int, prayers: QuerySet) -> Union[Answer, List[Answer]]:
    """Функция должна генерировать новы PrayerAtUser или возвращать те, которые уже есть.

    TODO подумать над названием (сгенерировать или вернуть то, что есть)
    TODO сделать тест на разные дни
    """
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
    """Возвращает эмоджи для кнопки в зависимости от того, прочитан намаз или нет."""
    return '❌' if not prayer.is_read else '✅'


def get_buttons(
    subscriber: Subscriber = None,
    prayer_times: QuerySet = None,
    prayer_at_user_pk: int = None,
) -> List[List[Tuple[str, str]]]:
    """Возвращает кнопки со статусом намазов.

    TODO если пользователь получил 2 времени намаза в разных городах в один день, вероятно будет ошибка
    """
    text_for_read_prayer = 'set_prayer_status_to_unread({})'
    text_for_unread_prayer = 'set_prayer_status_to_read({})'
    if prayer_at_user_pk:
        day = PrayerAtUser.objects.get(pk=prayer_at_user_pk).prayer.day
        subscriber = PrayerAtUser.objects.get(pk=prayer_at_user_pk).subscriber
        prayers = PrayerAtUser.objects.filter(subscriber=subscriber, prayer__day=day).order_by('pk')
    else:
        prayers = generate_prayer_at_user(subscriber.tg_chat_id, prayer_times.order_by('pk'))
    buttons = []
    for x in prayers:
        handle_text = text_for_read_prayer.format(x.pk) if x.is_read else text_for_unread_prayer.format(x.pk)
        buttons.append(
            (get_emoji_for_button(x), handle_text),
        )
    return [buttons]


def get_text_prayer_times(prayer_times: QuerySet, city_name: str, date: datetime) -> str:
    """Преобразует QuerySet намазов в текст для отправки пользователю."""
    res = f'Время намаза для г. {city_name} ({date.strftime("%d.%m.%Y")}) \n\n'
    for i in range(6):
        prayer = prayer_times[i]
        if settings.RAMADAN_MODE and i == 0:
            res += f'{prayer.get_name_display()}: {prayer.time.strftime("%H:%M")} <i> - Конец сухура</i>\n'
        elif settings.RAMADAN_MODE and i == 4:
            res += f'{prayer.get_name_display()}: {prayer.time.strftime("%H:%M")} <i> - Ифтар</i>\n'
        else:
            res += f'{prayer.get_name_display()}: {prayer.time.strftime("%H:%M")}\n'
    return res


def send_prayer_time(date: datetime = None) -> None:
    """Рассылаем время намаза с кнопками.

    TODO написать тесты
    TODO Переписать на сервисный объект
    TODO одинаковы куски кода content.service.do_morning_content_distribution
    """
    if date is None:
        date = (datetime.today() + timedelta(days=1))
    mailing = Mailing.objects.create()
    try:
        for subscriber in Subscriber.objects.filter(city__isnull=False, is_active=True):
            prayer_times = get_prayer_time(subscriber.city, date)
            logger.debug(f'{prayer_times=}')
            text = get_text_prayer_times(prayer_times, subscriber.city.name, date)
            logger.debug(f'{text=}')
            keyboard = InlineKeyboard(get_buttons(subscriber, prayer_times.exclude(name='sunrise'))).keyboard
            message_instance = Answer(text, keyboard=keyboard).send(subscriber.tg_chat_id)

            message_instance.mailing = mailing
            message_instance.save(update_fields=['mailing'])
        text = f'Рассылка #{mailing.pk} завершена'
        msg = send_message_to_admin(text)
        msg.mailing = mailing
        msg.save(update_fields=['mailing'])
    except Exception as e:
        logger.error(
            f'Subscriber: {subscriber}, city: {subscriber.city}, dont send prayer time. Error message: {str(e)}',
        )


def get_now_prayer(chat_id: int, date_time: datetime = None) -> Prayer:
    """Получаем текущий намаз."""
    date_time = date_time if date_time is not None else datetime.now()
    prayer_time = time(hour=date_time.hour, minute=date_time.minute)
    prayer = Prayer.objects.filter(
        day__date=date_time,
        city__subscriber__tg_chat_id=chat_id,
        time__lt=prayer_time,
    ).last()
    return prayer


def get_unread_prayers_by_chat_id(chat_id: int, date_time: datetime = None) -> QuerySet:
    """Получаем непрочитанные намазы у подписчика."""
    date_time = date_time if date_time is not None else datetime.now()
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    unread_prayers = PrayerAtUser.objects.filter(
        subscriber=subscriber,
        is_read=False,
        prayer__day__date__lte=date_time,
        prayer__time__lt=date_time.time(),
    ).order_by('-pk')[1:]
    return unread_prayers


def unread_prayer_type_minus_one(chat_id: int, prayer_type_id: int) -> None:
    """Уменьшаем кол-во непрочитанных намазов отдельной категории на один."""
    unread_prayers = get_unread_prayers_by_chat_id(chat_id)
    prayer_name = PRAYER_NAMES[prayer_type_id][0]
    separate_unread_prayer = unread_prayers.filter(prayer__name=prayer_name).first()
    separate_unread_prayer.is_read = True
    separate_unread_prayer.save(update_fields=['is_read'])


def get_keyboard_for_unread_prayers(chat_id: int) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для непрочитанных намазов. Чтобы люди при нажатии могли уменьшать их кол-во."""
    buttons = []
    for prayer_type_id in [0, 2, 3, 4, 5]:
        prayer_name = PRAYER_NAMES[prayer_type_id][1]
        buttons.append(
            (
                (f'{prayer_name} - 1', f'unread_prayer_type_minus_one({prayer_type_id}, {chat_id})'),
            ),
        )
    return InlineKeyboard(buttons).keyboard


def get_unread_prayers(chat_id: int) -> Answer:
    """Возвращает кол-во непрочитанных намазов с клавиатурой."""
    text = 'Не прочитано\n\n'
    unread_prayers = get_unread_prayers_by_chat_id(chat_id)
    for i in [0, 2, 3, 4, 5]:
        prayer_name = PRAYER_NAMES[i][0]
        prayer_type_group = [prayer for prayer in unread_prayers if prayer.prayer.name == prayer_name]
        text += f'{PRAYER_NAMES[i][1]}: {len(prayer_type_group)}\n'
    return Answer(text, keyboard=get_keyboard_for_unread_prayers(chat_id))


def get_prayer_time_or_no(chat_id: int) -> Answer:
    """Возвращает ответ с временами намазов или приглашением к поиску, если не установлен город."""
    subscriber = get_subscriber_by_chat_id(chat_id)
    if subscriber.city is None:
        return get_city_not_found_answer(
            text='Вы не указали город, отправьте местоположение или воспользуйтесь поиском',
        )
    today = datetime.now()
    prayers = get_prayer_time(subscriber.city, today)
    text = get_text_prayer_times(prayers, subscriber.city.name, today)
    keyboard = InlineKeyboard(get_buttons(subscriber, prayers)).keyboard
    return Answer(text, keyboard=keyboard)

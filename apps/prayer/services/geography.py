import pytz
from geopy import GeoNames, Nominatim
from loguru import logger

from apps.bot_init.models import Subscriber
from apps.bot_init.service import get_subscriber_by_chat_id
from apps.bot_init.services.answer_service import Answer
from apps.prayer.exceptions.city_non_exist import CityNonExist
from apps.prayer.models import City
from apps.prayer.service import get_city_not_found_answer


def set_city_to_subscriber(city: City, chat_id: int) -> Answer:
    """Присваивает город подписчику по инстансу города и идентификатору чата с пользователем."""
    subscriber = get_subscriber_by_chat_id(chat_id)
    subscriber.city = city
    subscriber.save(update_fields=['city'])
    return Answer(f'Вам будет приходить время намаза для г. {city.name}')


def get_address(x: str, y: str) -> str:
    """Получаем адрес по координатам благодаря библиотеке geopy."""
    geolocator = Nominatim(user_agent='qbot')
    location = geolocator.reverse(f'{x}, {y}')
    return location.address


def get_city_timezone(city_name: str) -> pytz:
    """Получить часовой пояс города."""
    geolocator = Nominatim(user_agent='qbot')
    if location := geolocator.geocode(city_name):
        _, (lat, lng) = location
    else:
        raise CityNonExist
    timezone = GeoNames(username='blablatdinov').reverse_timezone(query=(lat, lng))
    logger.debug(f'Timezone for {city_name}={timezone}')
    return pytz.timezone(str(timezone.pytz_timezone))


def set_city_to_subscriber_by_location(location: tuple, chat_id: int) -> Answer:
    """Ищем город и если не находим, то предлагаем пользователю найти в поиске."""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    address = get_address(location[0], location[1])

    address_split = address.replace(', ', ' ').split(' ')
    for elem in address_split:
        if city := City.objects.filter(name__contains=elem).first():
            answer = set_city_to_subscriber(city, subscriber.tg_chat_id)
            return answer
    logger.info(f'Finded city {location}, {address}')
    return get_city_not_found_answer()

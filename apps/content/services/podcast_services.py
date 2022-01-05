from django.db.models import QuerySet
from loguru import logger

from apps.content.models import Podcast


def get_random_podcast() -> QuerySet[Podcast]:
    """Получить Queryset с одним случайным подкастом."""
    random_podcast_queryset = Podcast.objects.order_by('?')[0:1]
    return random_podcast_queryset


def get_random_podcast_instance() -> Podcast:
    """Возвращает случайный подкаст."""
    podcast = Podcast.objects.order_by('?').first()
    logger.debug(podcast)
    return podcast

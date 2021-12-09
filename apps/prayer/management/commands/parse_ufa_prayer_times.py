from django.core.management.base import BaseCommand

from apps.prayer.parsers.ufa_prayer_time_parsers import PrayerTimeParser


class Command(BaseCommand):
    """Спарсить времена намазов с сайта namaz-time.ru."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        PrayerTimeParser()()

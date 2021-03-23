from django.core.management.base import BaseCommand

from apps.prayer.parsers.ufa_prayer_time_parsers import PrayerTimeParser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        PrayerTimeParser()()

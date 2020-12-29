from django.core.management.base import BaseCommand

from apps.prayer.parsers import prayer_time_parser
from apps.prayer.service import send_prayer_time


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        prayer_time_parser()

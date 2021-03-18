from datetime import datetime

from django.core.management.base import BaseCommand

from apps.prayer.service import send_prayer_time
from apps.prayer.parsers import get_time_by_str


class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser):
    #     parser.add_argument('time', type=str)

    def handle(self, *args, **options):
        # time = get_time_by_str(options['time']) or None
        send_prayer_time()

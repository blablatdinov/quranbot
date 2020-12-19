from datetime import datetime

from django.core.management.base import BaseCommand

from prayer.service import send_prayer_time
from prayer.parsers import get_time_by_str


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('time', type=str)

    def handle(self, *args, **options):
        time = get_time_by_str(options['time'])
        send_prayer_time(time)

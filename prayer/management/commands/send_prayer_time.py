from django.core.management.base import BaseCommand

from prayer.service import send_prayer_time


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        send_prayer_time()

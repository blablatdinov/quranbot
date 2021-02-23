from django.core.management.base import BaseCommand

from apps.prayer.parsers import prayer_time_parser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        prayer_time_parser()

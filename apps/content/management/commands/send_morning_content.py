from django.core.management.base import BaseCommand, CommandError

from apps.content.service import do_morning_content_distribution


class Command(BaseCommand):
    help = 'command for manual send morning content'

    def handle(self, *args, **options):
        do_morning_content_distribution()

from django.core.management.base import BaseCommand

from apps.content.parsers import run_parser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        run_parser()

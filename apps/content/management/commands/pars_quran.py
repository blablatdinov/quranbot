from django.core.management.base import BaseCommand

from apps.content.parsers import run_parser


class Command(BaseCommand):
    """Команда для парсинга аятов."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        run_parser()

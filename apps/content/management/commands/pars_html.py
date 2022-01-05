from django.core.management.base import BaseCommand

from apps.content.parsers import AyatParser


class Command(BaseCommand):
    """Команда для парсинга аятов из html в БД."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        p = AyatParser()
        p.parse_content_from_db()

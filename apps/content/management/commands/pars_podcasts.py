from django.core.management.base import BaseCommand

from apps.content.podcast_parser import PodcastParser


class Command(BaseCommand):
    """Команда для парсинга подкастов."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        PodcastParser()()

from django.core.management.base import BaseCommand

from apps.content.service import do_morning_content_distribution


class Command(BaseCommand):
    """Command for manual send morning content."""

    help = 'command for manual send morning content'

    def handle(self, *args, **options):
        """Entrypoint."""
        do_morning_content_distribution()

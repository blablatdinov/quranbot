from django.core.management.base import BaseCommand

from apps.prayer.service import send_prayer_time


class Command(BaseCommand):
    """Команда для отправки времени намаза."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        send_prayer_time()

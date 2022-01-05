from django.core.management.base import BaseCommand

from apps.bot_init.service import commit_concourse, count_active_users


class Command(BaseCommand):
    """Команда, для определения победителей конкурса."""

    help = ''

    def handle(self, *args, **options):
        """Entrypoint."""
        if input(
            'Перед запуском этой команды нужно проверить кол-во активных пользователей. Запустить проверку [y/N]:',
        ) == 'y':
            count_active_users()
        commit_concourse()

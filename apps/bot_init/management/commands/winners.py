from django.core.management.base import BaseCommand
from loguru import logger

from apps.bot_init.service import commit_concourse, count_active_users


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        if input("Перед запуском этой команды нужно проверить кол-во активных пользователей. Запустить проверку [y/N]:") == "y":
            count_active_users()
        commit_concourse()

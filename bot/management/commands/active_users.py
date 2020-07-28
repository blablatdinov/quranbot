from django.core.management.base import BaseCommand, CommandError

from bot.models import Subscribers
from bot.views import tbot


class Command(BaseCommand):
    help = 'command return count of active users'

    def handle(self, *args, **options):
        count = 0
        for sub in Subscribers.objects.all():
            try:
                tbot.send_chat_action(sub.telegram_chat_id, 'typing')
                sub.status = True
                sub.save()
                count += 1
            except:
                pass
        #count = Subscribers.objects.filter(status=True).count()
        print(f'Count of active users - {count}')

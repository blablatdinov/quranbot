from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot_init.models import Message


class GetPingToMessage(APIView):

    def get(self, request):
        now_datetime = timezone.now()
        messages = Message.objects.filter(date__lte=now_datetime).exclude(is_unknown=True).order_by('message_id')
        for index, mess in enumerate(messages):
            if mess.from_user_id != settings.TG_BOT.id:
                break

        sum_time_ping = timedelta(0)
        for i in range(index, messages.count(), 2):
            from loguru import logger
            logger.debug(f'{messages[i].date=} {messages[i + 1].date=}')
            delta = messages[i].date - messages[i + 1].date
            sum_time_ping += delta

        return Response({'seconds': sum_time_ping / (messages.count() / 2)}, status=200)

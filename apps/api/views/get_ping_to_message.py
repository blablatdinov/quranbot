from functools import reduce
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings

from apps.bot_init.models import Message


class GetPingToMessage(APIView):

    def get(self, request):
        now_datetime = timezone.now()
        messages = Message.objects.filter(date__lte=now_datetime).exclude(is_unknown=True).order_by('message_id')
        result = 0
        for index, mess in enumerate(messages):
            if mess.from_user_id != settings.TG_BOT.id:
                break
        sum_time_ping = timedelta(0)
        for i in range(index, messages.count(), 2):
            from loguru import logger
            logger.debug(f'{messages[i].date=} {messages[i + 1].date=}')
            delta = messages[i].date - messages[i + 1].date
            sum_time_ping += delta
        
        from loguru import logger
        logger.debug(f'{sum_time_ping=}')
        # list_times = list(map(lambda x: x.date, messages[index:]))
        # from loguru import logger
        # logger.debug(f'{list_times=}')
        # sum_ping_time = reduce(lambda x, y: x + y, list_times)
        # print(sum_ping_time)
        return Response({'seconds': sum_time_ping / (messages.count() / 2)}, status=200)
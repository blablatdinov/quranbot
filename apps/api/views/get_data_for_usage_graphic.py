import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.conf import settings

from apps.bot_init.models import Message


class GetDataForUsageGraphicSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format='%Y-%m-%d')
    message_count = serializers.IntegerField()


class GetDataForUsageGraphic(APIView):

    def get(self, request):
        dates_range = request.GET.get('dates_range') or '2021-07-01,2021-07-29'
        start_date, end_date = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in dates_range.split(',')]
        delta = datetime.timedelta(days=1)
        from loguru import logger
        logger.debug(f'{dates_range=}')
        result = []
        while start_date <= end_date:
            result.append({
                'date': start_date,
                'message_count': Message.objects.filter(date__range=(start_date, start_date + datetime.timedelta(days=1))).exclude(from_user_id=settings.TG_BOT.id).count()
            })
            start_date += delta
        return Response(
            GetDataForUsageGraphicSerializer(result, many=True).data,
            status=200,
        )

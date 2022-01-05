import datetime

import pendulum
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot_init.models import Message


class GetDataForUsageGraphicSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format='%Y-%m-%d')
    message_count = serializers.IntegerField()


class GetDataForUsageGraphic(APIView):

    def get(self, request):
        dates_range = request.GET.get('dates_range')
        start_date, end_date = [
            pendulum.parse(x, tz='Europe/Moscow')
            for x in dates_range.split(',')
        ]
        delta = datetime.timedelta(days=1)
        result = []

        while start_date <= end_date:
            date_range = (
                start_date,
                start_date.add(days=1).subtract(seconds=1),
            )
            messages_count = (
                Message.objects
                .filter(date__range=date_range)
                .exclude(from_user_id=settings.TG_BOT.id)
                .count()
            )
            result.append({
                'date': start_date.format('YYYY-MM-DD'),
                'message_count': messages_count,
            })
            start_date += delta
        return Response(
            result,
            status=200,
        )

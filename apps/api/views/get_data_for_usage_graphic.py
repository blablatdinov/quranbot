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
        if not dates_range:
            end_date = pendulum.now(tz=settings.TIME_ZONE)
            start_date = end_date.subtract(days=7)
        else:
            start_date, end_date = [
                pendulum.parse(x, tz=settings.TIME_ZONE)
                for x in dates_range.split(',')
            ]
        period = pendulum.period(start_date, end_date)
        messages = (
            Message.objects
            .filter(date__range=(period.start, period.end))
            .order_by('date')
            .exclude(from_user_id=settings.TG_BOT.id)
        )

        result = []
        for dt in period.range('days'):
            result.append({
                'date': dt.format('YYYY-MM-DD'),
                'message_count': len(tuple(filter(
                    lambda mess: dt <= mess.date < dt.add(days=1), messages,
                ))),
            })

        return Response(
            result,
            status=200,
        )

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot_init.models import Subscriber


class GetSubscribersCount(APIView):

    def get(self, request):
        return Response({
            'active': Subscriber.objects.filter(is_active=True).count(),
            'all': Subscriber.objects.count(),
        })

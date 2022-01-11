from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot_init.service import calculate_message_ping


class GetPingToMessage(APIView):

    def get(self, request):
        return Response({'seconds': calculate_message_ping()})

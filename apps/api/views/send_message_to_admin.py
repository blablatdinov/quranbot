from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot_init.service import send_message_to_admin


class SendMessageToAdmin(APIView):

    def post(self, request):
        message_text = request.data['text']
        send_message_to_admin(message_text)
        return Response(status=200)

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.bot_init.service import send_message_to_admin
from apps.bot_init.utils import save_message


class SendMessageToAdmin(APIView):

    def post(self, request):
        message_text = request.data['text']
        message = send_message_to_admin(message_text)
        return Response(status=200)

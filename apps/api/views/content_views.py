from rest_framework.views import APIView
from rest_framework.response import Response

from apps.api.services.content.content_service import get_morning_content


class ContentView(APIView):

    def get(self, request):
        res = get_morning_content()
        return Response(res)
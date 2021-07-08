from rest_framework.views import APIView
from rest_framework.response import Response

from apps.content.services.create_morning_content import MorningContentCreator
from apps.api.serializers import MorningContentCreateSerializer, MorningContentSerializer


class MorningContentView(APIView):
    serializer_class = MorningContentCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        morning_content = MorningContentCreator(
            day=serializer.data['day'],
            ayats_ids=serializer.data['ayats_ids'],
        )()
        serializer = MorningContentSerializer(morning_content)
        return Response(serializer.data, status=201)

from django.db.models import Q
from rest_framework.generics import ListAPIView

from apps.api.serializers import MessageShortSerializer
from apps.bot_init.models import Message
from apps.bot_init.services.getting_messages import get_messages


class MessagesView(ListAPIView):
    serializer_class = MessageShortSerializer

    def get_queryset(self):
        return get_messages(
            self.request.GET.get('q'),
            self.request.GET.get('in_mailing'),
            self.request.GET.get('is_unknown'),
        )

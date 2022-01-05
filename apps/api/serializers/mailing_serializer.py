from rest_framework import serializers

from apps.bot_init.models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    recipients_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mailing
        fields = (
            'id',
            'is_cleaned',
            'recipients_count',
        )

    def get_recipients_count(self, mailing: Mailing) -> int:
        return mailing.messages.count()


class MailingCreateSerializer(serializers.Serializer):
    text = serializers.CharField()

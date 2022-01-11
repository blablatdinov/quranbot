from rest_framework import serializers

from apps.bot_init.models import Mailing, Message


class MessageShortSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'date',
            'from_user_id',
            'chat_id',
            'mailing',
            'is_unknown',
            'text',
            'message_id',
        )

    def get_text(self, message: Message) -> str:
        message_truncate_len = 20
        if len(message.text) > message_truncate_len:
            return message.text[:message_truncate_len] + '...'

        return message.text

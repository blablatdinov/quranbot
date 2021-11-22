from rest_framework import serializers

from apps.api.serializers.ayat_serializer import AyatSerializer
from apps.content.models import MorningContent


class MorningContentCreateSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    ayats_ids = serializers.ListField()


class MorningContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    related_ayats = AyatSerializer(many=True, source='ayat_set')
    content_length = serializers.SerializerMethodField()

    class Meta:
        model = MorningContent
        fields = [
            'id',
            'day',
            'content_length',
            'related_ayats',
        ]

    def get_content_length(self, obj):
        return len(obj.content_for_day())

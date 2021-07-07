from rest_framework import serializers

from apps.content.models import MorningContent
from apps.api.serializers.ayat_serializer import AyatSerializer


class MorningContentCreateSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    ayats_ids = serializers.ListField()


class MorningContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    related_ayats = AyatSerializer(many=True, source='ayat_set')

    class Meta:
        model = MorningContent
        fields = [
            'id',
            'related_ayats',
        ]
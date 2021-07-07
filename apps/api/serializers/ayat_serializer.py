from rest_framework import serializers

from apps.content.models import Ayat


class AyatSerializer(serializers.ModelSerializer):
    sura = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk')

    class Meta:
        fields = [
            'id',
            'additional_content',
            'content',
            'arab_text',
            'trans',
            'sura',
            'ayat',
        ]
        model = Ayat

    def get_sura(self, obj):
        return obj.sura.number



class AyatListSerializer(serializers.ModelSerializer):
    sura = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk')

    class Meta:
        fields = [
            'id',
            'content',
            'sura',
            'ayat',
        ]
        model = Ayat

    def get_sura(self, obj):
        return obj.sura.number

from rest_framework import serializers

from apps.content.models import Ayat


class AyatSerializer(serializers.ModelSerializer):
    sura = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk')
    content_day = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id',
            'additional_content',
            'content',
            'arab_text',
            'trans',
            'sura',
            'ayat',
            'link',
            'content_day',
            'html',
        ]
        model = Ayat

    def get_content_day(self, obj):
        try:
            return obj.one_day_content.day
        except AttributeError:
            return None

    def get_sura(self, obj):
        return obj.sura.number

    def get_link(self, obj):
        return f'https://umma.ru{obj.sura.link}'


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

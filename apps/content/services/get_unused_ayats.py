from apps.content.models import Ayat


def get_unused_ayats():
    return Ayat.objects.filter(one_day_content__isnull=True).prefetch_related('sura').order_by('pk')

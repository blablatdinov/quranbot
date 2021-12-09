from apps.content.models import Ayat


def get_unused_ayats():
    """Получить аяты, которые еще не используются в утреннем контенте."""
    return Ayat.objects.filter(one_day_content__isnull=True).prefetch_related('sura').order_by('pk')

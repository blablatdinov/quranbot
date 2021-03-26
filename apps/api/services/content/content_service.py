from apps.content.models import MorningContent, Ayat


def get_morning_content(limit: int = 10):
    morning_content = [
        {
            "day": x.day,
            "content": x.content_for_day()
        }
        for x in MorningContent.objects.all().order_by("-pk")[:limit]
    ]
    return morning_content


def get_ayats_by_sura_number(sura_number):
    ayats = [
        {
            "pk": ayat.pk,
            "sura": ayat.sura,
            "ayat": ayat.ayat,
            "content_length": len(ayat.content)
        }
        for ayat in Ayat.objects.filter(one_day_content__isnull=True, sura=sura_number).order_by("pk")
    ]

    return ayats
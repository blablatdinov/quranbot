from loguru import logger

from apps.content.models import Ayat


def get_ayat_by_sura_ayat_numbers(sura_number, ayat_number):
    # TODO добавить тест на поиск 2:1
    if sura_number and ayat_number:
        logger.info(f"Search {sura_number}:{ayat_number}")
        queryset = Ayat.objects.filter(sura__number=sura_number, ayat=ayat_number)
        return queryset
    queryset = Ayat.objects.all()
    return queryset
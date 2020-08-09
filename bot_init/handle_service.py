# TODO создать папку для бизнес логики
import re

from bot_init.text_message_service import translate_ayat_into_answer
from content.models import Ayat


def handle_query_service(text: str):
    if 'get_ayat' in text:
        ayat_pk = re.search(r'\d+', text).group(0)
        ayat = Ayat.objects.get(pk=ayat_pk)
        answer = translate_ayat_into_answer(ayat)
        return answer

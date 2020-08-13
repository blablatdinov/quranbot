from django.test import TestCase

from bot_init.services.text_message_service import *
from bot_init.models import Ayat


class GetAyatByTextTestCase(TestCase):

    def test_first(self):
        pairs = ['1:1-7', '2:1-5', '4:67, 68', '4:12', '5:1, 3']
        for elem in pairs:
            Ayat.objects.create(
                content='asdf',
                arab_text='asdf',
                trans='asdf',
                sura=int(elem.split(':')[0]),
                ayat=elem.split(':')[1],
                html='<html></html>',
            )
        test_data = ['1:1', '2:4', '4:67', '4:12']
        for i in range(4):
            res1 = Ayat.objects.get(pk=i + 1)
            res2 = get_ayat_by_sura_ayat(test_data[i])
            self.assertEqual(res1, res2)
        try:
            get_ayat_by_sura_ayat('5:2')
        except AyatDoesNotExists:
            self.assertEqual(True, True)


class TranslateAyatIntoAnswerTestCase(TestCase):

    def test_ok(self):
        audio = AudioFile.objects.create(audio_link='some_link')
        a1 = Ayat.objects.create(
            content='asdf', arab_text='asdf', trans='asdf', sura=7, ayat='10', html='<html></html>', audio=audio
        )
        Ayat.objects.create(
            content='asdf', arab_text='asdf', trans='asdf', sura=7, ayat='15', html='<html></html>',
        )
        res = translate_ayat_into_answer(a1)
        text_for_a1 = f'<b>({a1.sura}:{a1.ayat})</b>\n{a1.arab_text}\n\n{a1.content}\n\n<i>{a1.trans}</i>\n\n'
        self.assertEqual(text_for_a1, res[0].text)
        keyboard_for_a1 = get_keyboard_for_ayat(a1)
        self.assertEqual(keyboard_for_a1.to_json(), res[0].keyboard.to_json())
        audio_for_a1 = get_audio_answer(a1.audio)
        self.assertEqual(audio.audio_link, audio_for_a1.text)

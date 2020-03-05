def save_message(msg):
    from datetime import datetime
    from django.utils.timezone import make_aware
    from bot.models import Message
    import json
    from pprint import pprint
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = eval(msg.__str__())
    except:
        json_str = msg.__str__()
    json = json.dumps(json_str, indent=2, ensure_ascii=False)
    Message.objects.create(date=date, from_user_id=from_user_id, message_id=message_id,
                           chat_id=chat_id, text=text, json=json)



def get_arab_text(soup):
    return soup.find('div', class_='quran-speaker').text


def clean_content(text):
    import re
    return re.sub(r'\[\d\]+', '', text)


def get_trans(soup):
    return soup.find('div', class_='transcription').text


def get_audio(soup):
    return soup.find('div', class_='quran-speaker')['data-audio']


def pars_ayatss():
    from .models import QuranAyat
    from bs4 import BeautifulSoup

    qs = QuranAyat.objects.all()
    for q in qs:
        html = q.html
        soup = BeautifulSoup(html, 'lxml')
        #q.content = soup.find('div', class_='text').find('p').text
        h3 = soup.find('h3').text.split(':')
        #q.arab_text = get_arab_text(soup)
        #q.trans = get_trans(soup)
        q.audio_link = get_audio(soup)
        #q.sura = h3[0]
        #q.ayat = h3[1]
        q.save()
        print(h3)


def save_mp3():
    from bot.models import Audio
    from bot.views import tbot
    import requests
    import sys
    import json
    import progressbar
    with open('audio.json', 'r') as f:
        data = json.load(f)[994:]
    #audios = Audio.objects.all()[554:]
    #for audio in audios:
    for i in progressbar.progressbar(range(len(data))):
        link = data[i]['audio_link']
        audio = Audio(title=data[i]['title'])
        #try:
        r = requests.get(link)
        if sys.getsizeof(r.content) < 50 * 1024 * 1024:
            msg = tbot.send_audio(358610865, r.content, timeout=180, title=audio.title, performer='Шамиль Аляутдинов')
            audio.tg_audio_link = msg.audio.file_id
            audio.save()
            tbot.delete_message(358610865, msg.message_id)
        else:
            pass


def save_ayat_audio():
    from bot.models import QuranAyat
    from bot.views import tbot
    import requests
    ayats = QuranAyat.objects.all()
    for ayat in ayats:
        r = requests.get(ayat.audio_link)
        msg = tbot.send_audio(358610865, r.content, title=f'{ayat.sura}:{ayat.ayat}', performer='umma.ru')
        ayat.tg_audio_link = msg.audio.file_id
        print(f'{ayat.pk}) {ayat.sura}:{ayat.ayat}')
        print(ayat.tg_audio_link)
        ayat.save()
        tbot.delete_message(358610865, msg.message_id)


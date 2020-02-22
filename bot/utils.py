def write_audio(audio_title, audio_link):
    import csv
    from bot.models import Audio

    n = 0
    with open('audio.csv', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        for row in data:
            if n % 2 == 0:
                a = Audio.objects.create(title=row[0], audio_link=row[1])
                a.save()
                print(n/2)
            n += 1


def write_ayats():
    from .models import QuranAyat
    with open('output.txt', 'r', encoding='utf-8') as f:
        while True:
            line = eval(f.readline())
            q = QuranAyat(html=line[1])
            q.save()
            print(line[0])


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
        #print(get_audio(soup))
        #print(h3)
        #q.arab_text = get_arab_text(soup)
        #q.trans = get_trans(soup)
        q.audio_link = get_audio(soup)
        #print(q.arab_text)
        #q.sura = h3[0]
        #q.ayat = h3[1]
        q.save()
        print(h3)


def save_mp3():
    from bot.models import Audio
    from bot.views import tbot
    import requests
    import sys
    audios = Audio.objects.all()[554:]
    for audio in audios:
        #try:
        r = requests.get(audio.audio_link)
        if sys.getsizeof(r.content) < 50 * 1024 * 1024:
            msg = tbot.send_audio(358610865, r.content, timeout=180, title=audio.title, performer='Шамиль Аялутдинов')
            audio.tg_audio_link = msg.audio.file_id
            print(f'{audio.pk}: {audio.title}')
            print(audio.tg_audio_link)
            audio.save()
            tbot.delete_message(358610865, msg.message_id)
        else:
            pass
        #except:
        #print(f'problem with audion\npk: {audio.pk}\ntitle: {audio.title}')


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


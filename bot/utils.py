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


def pars_ayatss():
    from .models import QuranAyat
    from bs4 import BeautifulSoup
    
    qs = QuranAyat.objects.all()
    for q in qs:
        html = q.html
        soup = BeautifulSoup(html, 'lxml')
        #q.content = soup.find('div', class_='text').find('p').text
        h3 = soup.find('h3').text.split(':')
        print(h3)
        #q.arab_text = get_arab_text(soup)
        q.trans = get_trans(soup)
        print(q.trans)
        #print(q.arab_text)
        #q.sura = h3[0]
        #q.ayat = h3[1]
        q.save()


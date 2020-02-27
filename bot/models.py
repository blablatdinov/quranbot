from django.db import models


class QuranAyatManager(models.Manager):

    def get_ayat(self, mes):
        sura = int(mes.split(':')[0])
        if 1 > sura > 114:
            return 'Сура не найдена'
        ayat = int(mes.split(':')[1])
        sura_ayats = self.filter(sura=sura)
        for sa in sura_ayats:
            sa_str = sa.__str__()
            sa_str_ayats = sa_str.split(':')[1]
            if '-' in sa_str:
                first_range_ayat = int(sa_str_ayats.split('-')[0])
                second_range_ayat = int(sa_str_ayats.split('-')[1])
                if ayat in range(first_range_ayat, second_range_ayat + 1):
                    print(sa_str)
                    return sa
            elif ',' in sa_str_ayats:
                s = [int(x) for x in sa_str_ayats.split(',')]
                if ayat in s:
                    print(s)
                    return sa
            elif int(sa.ayat) == ayat:
                return sa
        return 'Аят не найден'


class QuranOneDayContent(models.Model):
    content = models.TextField(blank=True)
    day = models.IntegerField()

    def __str__(self):
        return f'{self.day} день'

    def content_for_day(self):
        quran_qs = QuranAyat.objects.filter(one_day_content__day=self.day).order_by('pk')
        result = ''
        if self.content is not '':
            result += f'{self.content}\n\n'
        for q in quran_qs:
            result += f'*{q.sura}:{q.ayat})* {q.content}\n'
        return result

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей:'
        verbose_name_plural = 'Ежедневный контент для пользователей:'


class QuranAyat(models.Model):
    content = models.TextField(blank=True)
    arab_text = models.TextField(blank=True)
    trans = models.TextField(blank=True)
    audio_link = models.CharField(max_length=512)
    tg_audio_link = models.CharField(max_length=512)
    sura = models.IntegerField(blank=True, null=True)
    ayat = models.CharField(max_length=16, blank=True)
    html = models.TextField(blank=True)
    one_day_content = models.ForeignKey(QuranOneDayContent, blank=True, null=True, on_delete=models.CASCADE)

    objects = QuranAyatManager()

    def get_content(self):
        return f'*({self.sura}:{self.ayat})*\n{self.arab_text}\n\n{self.content}\n\n**{self.trans}**\n\n'

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана:'
        verbose_name_plural = 'Аяты Священного Корана:'


class Subscribers(models.Model):
    telegram_chat_id = models.IntegerField()
    day = models.IntegerField()
    status = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.telegram_chat_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Audio(models.Model):
    """Модель для аудио подкаста"""
    title = models.CharField(max_length=128)
    audio_link = models.CharField(max_length=512)
    tg_audio_link = models.CharField(max_length=512)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аудио подкаст'
        verbose_name_plural = 'Аудио подкасты'


class Message(models.Model):
    """ Модель для хранения сообщеинй """
    date = models.DateTimeField(blank=True, null=True)
    from_user_id = models.IntegerField()
    message_id = models.IntegerField()
    chat_id = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    json = models.TextField()

    def __str__(self):
        if self.from_user_id == 705810219:
            return 'From bot'
        else:
            return 'To bot'

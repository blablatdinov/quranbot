from django.db import models


class QuranOneDayContent(models.Model):
    content = models.TextField(blank=True)
    #sura_ayat = models.ForeignKey(QuranAyat, blank=True, on_delete=models.CASCADE)
    day = models.IntegerField()

    def __str__(self):
        return f'{self.day} день'

    def content_for_day(self):
        quran_qs = QuranAyat.objects.filter(one_day_content__day=self.day)
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
    ayat = models.CharField(max_length=5, blank=True)
    html = models.TextField(blank=True)
    one_day_content = models.ForeignKey(QuranOneDayContent, blank=True, null=True, on_delete=models.CASCADE)

    def get_content(self):
        return f'*({self.sura}:{self.ayat})*\n{self.arab_text}\n\n{self.content}\n\n**{self.trans}**\n\n' \
               f'Скоро будет аудио...'

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана:'
        verbose_name_plural = 'Аяты Священного Корана:'


class Subscribers(models.Model):
    telegram_chat_id = models.IntegerField()
    day = models.IntegerField()
    status = models.BooleanField(default=True)

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

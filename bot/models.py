from django.db import models


class QuranOneDayContent(models.Model):
    content = models.TextField(blank=True)
    #sura_ayat = models.ForeignKey(QuranAyat, blank=True, on_delete=models.CASCADE)
    day = models.IntegerField()

    def __str__(self):
        return f'{self.day} день'

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей:'
        verbose_name_plural = 'Ежедневный контент для пользователей:'



class QuranAyat(models.Model):
    content = models.TextField(blank=True)
    arab_text = models.TextField(blank=True)
    trans = models.TextField(blank=True)
    audio_link = ...
    tg_audio_link = ...
    sura = models.IntegerField(blank=True, null=True)
    ayat = models.CharField(max_length=5, blank=True)
    html = models.TextField(blank=True)
    one_day_content = models.ForeignKey(QuranOneDayContent, related_name='quran_ayats', blank=True, null=True, on_delete=models.PROTECT)

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

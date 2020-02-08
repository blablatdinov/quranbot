from django.db import models


class QuranAyat(models.Model):
    content = models.TextField(blank=True)
    arab_text = models.TextField(blank=True)
    trans = models.TextField(blank=True)
    audio_link = ...
    tg_audio_link = ...
    sura = models.IntegerField(blank=True)
    ayat = models.CharField(max_length=5, blank=True)
    html = models.TextField(blank=True)

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана:'
        verbose_name_plural = 'Аяты Священного Корана:'


class QuranOneDayContent(models.Model):
    content = models.TextField()
    sura_ayat = models.ForeignKey(QuranAyat, blank=True, on_delete=models.CASCADE)
    day = models.ForeignKey()

    def __str__(self):
        return f'{self.day} день'

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей:'
        verbose_name_plural = 'Ежедневный контент для пользователей:'


class Subscribers(models.Model):
    telegram_chat_id = models.IntegerField()
    day = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.telegram_chat_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

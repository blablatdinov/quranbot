from django.db import models


class QuranAyat(models.Model):
    content = models.TextField()
    sura = models.IntegerField()
    ayat = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана:'
        verbose_name_plural = 'Аяты Священного Корана:'


class QuranOneDayContent(models.Model):
    content = models.TextField()

    def __str__(self):
        return f'{self.pk} день'

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей:'
        verbose_name_plural = 'Ежедневный контент для пользователей:'


class Subscribers(models.Model):
    telegram_chat_id = models.IntegerField()
    day = models.ManyToManyField('QuranOneDayContent', blank=True, related_name='subscribers')

    def __str__(self):
        return str(self.telegram_chat_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

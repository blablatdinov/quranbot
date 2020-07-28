from django.db import models
# FIXME добавить verbose_name
# https://trello.com/c/z8B43BMW/25-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-verbosename-str-meta


class MorningContent(models.Model):
    additional_content = models.TextField(blank=True)
    day = models.IntegerField()

    def __str__(self):
        return f'{self.day} день'

    def content_for_day(self):  # TODO подумать насчет генерации контента
        ayats = Ayat.objects.filter(one_day_content__day=self.day).order_by('pk')
        result = ''
        if self.additional_content != '':
            result += f'{self.additional_content}\n\n'
        for ayat in ayats:
            result += f'<b>{ayat.sura}:{ayat.ayat})</b> {ayat.content}\n'
        if result != '':
            result += f'\nСсылка на источник: {ayats[0].link_to_source}'
        return result

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей'
        verbose_name_plural = 'Ежедневный контент для пользователей'


class AudioFile(models.Model):  # TODO добавить путь к файлу если есть
    audio_link = models.CharField(max_length=512)
    tg_audio_link = models.CharField(max_length=512)


class Ayat(models.Model):
    additional_content = models.TextField(blank=True)
    arab_text = models.TextField()
    trans = models.TextField()
    sura = models.IntegerField()
    ayat = models.CharField(max_length=16)
    html = models.TextField()
    audio = models.ForeignKey(AudioFile, on_delete=models.PROTECT)
    one_day_content = models.ForeignKey(MorningContent, blank=True, null=True, on_delete=models.SET_NULL)
    link_to_source = models.CharField(max_length=512)

    def get_content(self):
        return f'<b>({self.sura}:{self.ayat})</b>\n{self.arab_text}\n\n{self.content}\n\n<i>{self.trans}</i>\n\n'

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана'
        verbose_name_plural = 'Аяты Священного Корана'


class Podcast(models.Model):  # TODO adds field with description and other
    """Модель для аудио подкаста"""
    title = models.CharField(max_length=128)
    audio = models.ForeignKey(AudioFile, on_delete=models.PROTECT)
    is_flag = models.BooleanField(default=False, verbose_name='Последнее аудио за сессию парсинга')  # TODO naming

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аудио подкаст'
        verbose_name_plural = 'Аудио подкасты'

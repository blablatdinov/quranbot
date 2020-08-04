from django.db import models


class MorningContent(models.Model):
    """Утренний контент - аяты связанные в один день"""
    additional_content = models.TextField(blank=True, verbose_name='Дополнительный текст')
    day = models.IntegerField(verbose_name='День')

    def __str__(self):
        return f'{self.day} день'

    def content_for_day(self) -> str:  # TODO подумать насчет генерации контента
        """Возвращаем контент в виде строки для этого дня"""
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


class AudioFile(models.Model):
    # TODO добавить путь к файлу если есть, verbose_name, переименовать tg_audio_link -> tg_file_id
    audio_link = models.CharField(max_length=512, verbose_name='Ссылка на аудио')
    tg_audio_link = models.CharField(max_length=512, verbose_name='Идентификатор файла в телеграмм')

    def __str__(self):
        return self.audio_link


class Ayat(models.Model):
    """Аят священного Корана"""
    additional_content = models.TextField(blank=True, verbose_name='Допопнительный контент')
    content = models.TextField(verbose_name='Текст аята')
    arab_text = models.TextField(verbose_name='Арабский текст')
    trans = models.TextField(verbose_name='Транслитерация')
    sura = models.IntegerField(verbose_name='Номер суры')
    ayat = models.CharField(max_length=16, verbose_name='Номер аята')
    html = models.TextField(verbose_name='Спарсенный HTML текст')
    audio = models.ForeignKey(AudioFile, on_delete=models.PROTECT, verbose_name='Аудио файл')
    one_day_content = models.ForeignKey(
        MorningContent, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Ежедневный контент'
    )
    link_to_source = models.CharField(max_length=512, verbose_name='Ссылка на источник')

    def get_content(self) -> str:
        """Рендерим аят для отправки в HTML"""
        return f'<b>({self.sura}:{self.ayat})</b>\n{self.arab_text}\n\n{self.content}\n\n<i>{self.trans}</i>\n\n'

    def __str__(self):
        return f'{self.sura}:{self.ayat}'

    class Meta:
        verbose_name = 'Аят Священного Корана'
        verbose_name_plural = 'Аяты Священного Корана'


class Podcast(models.Model):  # TODO adds field with description and other
    """Модель для аудио подкаста"""
    title = models.CharField(max_length=128, verbose_name='Название')
    audio = models.ForeignKey(AudioFile, on_delete=models.PROTECT, verbose_name='Аудио файл')
    is_flag = models.BooleanField(default=False, verbose_name='Последнее аудио за сессию парсинга')  # TODO naming

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аудио подкаст'
        verbose_name_plural = 'Аудио подкасты'

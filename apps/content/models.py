"""Модели контента."""
from django.db import models

from apps.content.services.get_content_from_morning_content import get_content


class MorningContent(models.Model):
    """Утренний контент - аяты связанные в один день."""

    additional_content = models.TextField(blank=True, verbose_name='Дополнительный текст')
    day = models.IntegerField(verbose_name='День', unique=True)

    class Meta:
        verbose_name = 'Ежедневный контент для пользователей'
        verbose_name_plural = 'Ежедневный контент для пользователей'
        ordering = ['-day']

    def __str__(self) -> str:
        """Строковое представление."""
        return f'{self.day} день'

    def content_for_day(self) -> str:
        """Возвращаем контент в виде строки для этого дня.

        TODO подумать насчет генерации контента, сделать property
        """
        ayats = Ayat.objects.filter(one_day_content__day=self.day).order_by('pk')
        return get_content(ayats, self.additional_content)


class File(models.Model):
    """Модель файла."""

    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Имя файла')
    link_to_file = models.CharField(max_length=512, verbose_name='Ссылка на файл', blank=True, null=True)
    tg_file_id = models.CharField(
        max_length=512,
        verbose_name='Идентификатор файла в телеграмм',
        blank=True,
        null=True,
        help_text='Может быть пустым, т. к. некоторые файлы слишком велики для отправки.',
    )

    def __str__(self) -> str:
        """Строковое представление."""
        return self.link_to_file or self.tg_file_id


class Sura(models.Model):
    """Класс суры Корана."""

    number = models.IntegerField(verbose_name='Номер суры')
    pars_hash = models.CharField(
        max_length=64, blank=True, null=True, verbose_name='Хэш после предыдущей сессии парсинга',
    )
    link = models.CharField(max_length=128, verbose_name='Ссылка на суру')
    child_elements_count = models.IntegerField(verbose_name='Кол-во записей аятов в суре')

    def __str__(self) -> str:
        """Строковое представление."""
        return f'Сура {self.number}'


class Ayat(models.Model):
    """Аят священного Корана."""

    additional_content = models.TextField(blank=True, verbose_name='Дополнительный контент')
    content = models.TextField(verbose_name='Текст аята', blank=True)
    arab_text = models.TextField(verbose_name='Арабский текст', blank=True)
    trans = models.TextField(verbose_name='Транслитерация', blank=True)
    sura = models.ForeignKey(Sura, on_delete=models.CASCADE, verbose_name='Номер суры')
    # TODO отменить пустое значение
    ayat = models.CharField(max_length=16, verbose_name='Номер аята', blank=True, null=True)
    html = models.TextField(verbose_name='Спарсенный HTML текст')
    audio = models.OneToOneField(File, on_delete=models.PROTECT, verbose_name='Аудио файл', blank=True, null=True)
    one_day_content = models.ForeignKey(
        MorningContent, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Ежедневный контент',
    )

    class Meta:
        verbose_name = 'Аят Священного Корана'
        verbose_name_plural = 'Аяты Священного Корана'
        ordering = ['-id']

    def __str__(self) -> str:
        """Строковое представление."""
        return f'{self.sura.number}:{self.ayat}'

    def get_content(self) -> str:
        """Рендерим аят для отправки в HTML."""
        return f'<b>({self.sura.number}:{self.ayat})</b>\n{self.arab_text}\n\n{self.content}\n\n<i>{self.trans}</i>\n\n'


class Podcast(models.Model):
    """Модель для аудио подкаста.

    TODO adds field with description and other
    """

    title = models.CharField(max_length=128, verbose_name='Название')
    audio = models.OneToOneField(File, on_delete=models.PROTECT, verbose_name='Аудио файл')
    article_link = models.CharField(max_length=512, verbose_name='Ссылка на статью', blank=True, null=True)

    class Meta:
        verbose_name = 'Аудио подкаст'
        verbose_name_plural = 'Аудио подкасты'

    def __str__(self) -> str:
        """Строковое представление."""
        return self.title

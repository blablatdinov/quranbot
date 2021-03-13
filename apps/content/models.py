"""Модели контента."""
from django.db import models


class MorningContent(models.Model):
    """Утренний контент - аяты связанные в один день."""

    additional_content = models.TextField(blank=True, verbose_name="Дополнительный текст")
    day = models.IntegerField(verbose_name="День")

    class Meta:
        verbose_name = "Ежедневный контент для пользователей"
        verbose_name_plural = "Ежедневный контент для пользователей"

    def __str__(self):
        return f"{self.day} день"

    def content_for_day(self) -> str:  # TODO подумать насчет генерации контента, сделать property
        """Возвращаем контент в виде строки для этого дня."""
        ayats = Ayat.objects.filter(one_day_content__day=self.day).order_by("pk")
        result = ""
        if self.additional_content != "":
            result += f"{self.additional_content}\n\n"
        for ayat in ayats:
            result += f"<b>{ayat.sura.number}:{ayat.ayat})</b> {ayat.content}\n"
        if result != "":
            result += f"\nСсылка на источник: <a href='https://umma.ru{ayats[0].sura.link}'>umma.ru</a>"
        return result


class AudioFile(models.Model):
    """Модель аудиофайла."""

    # TODO добавить путь к файлу если есть, verbose_name
    audio_link = models.CharField(max_length=512, verbose_name="Ссылка на аудио")
    tg_file_id = models.CharField(max_length=512, verbose_name="Идентификатор файла в телеграмм", blank=True, null=True)

    def __str__(self):
        return self.audio_link


class Sura(models.Model):
    """Класс суры Корана."""

    number = models.IntegerField(verbose_name="Номер суры")
    pars_hash = models.CharField(
        max_length=64, blank=True, null=True, verbose_name="Хэш после предыдущей сессии парсинга"
    )
    link = models.CharField(max_length=128, verbose_name="Ссылка на суру")
    child_elements_count = models.IntegerField(verbose_name="Кол-во записей аятов в суре")

    def __str__(self):
        return f"Сура {self.number}"


class Ayat(models.Model):
    """Аят священного Корана."""

    additional_content = models.TextField(blank=True, verbose_name="Допопнительный контент")
    content = models.TextField(verbose_name="Текст аята", blank=True)
    arab_text = models.TextField(verbose_name="Арабский текст", blank=True)
    trans = models.TextField(verbose_name="Транслитерация", blank=True)
    sura = models.ForeignKey(Sura, on_delete=models.CASCADE, verbose_name="Номер суры")
    ayat = models.CharField(max_length=16, verbose_name="Номер аята", blank=True, null=True)
    html = models.TextField(verbose_name="Спарсенный HTML текст")
    audio = models.OneToOneField(AudioFile, on_delete=models.PROTECT, verbose_name="Аудио файл", blank=True, null=True)
    one_day_content = models.ForeignKey(
        MorningContent, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Ежедневный контент"
    )

    class Meta:
        verbose_name = "Аят Священного Корана"
        verbose_name_plural = "Аяты Священного Корана"

    def __str__(self):
        return f"{self.sura.number}:{self.ayat}"

    def get_content(self) -> str:
        """Рендерим аят для отправки в HTML."""
        return f"<b>({self.sura.number}:{self.ayat})</b>\n{self.arab_text}\n\n{self.content}\n\n<i>{self.trans}</i>\n\n"


class Podcast(models.Model):  # TODO adds field with description and other
    """Модель для аудио подкаста."""

    title = models.CharField(max_length=128, verbose_name="Название")
    audio = models.OneToOneField(AudioFile, on_delete=models.PROTECT, verbose_name="Аудио файл")
    article_link = models.CharField(max_length=512, verbose_name="Ссылка на статью", blank=True, null=True)

    class Meta:
        verbose_name = "Аудио подкаст"
        verbose_name_plural = "Аудио подкасты"

    def __str__(self):
        return self.title

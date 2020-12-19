"""Модели для модуля намаза"""
from django.db import models

from apps.bot_init.models import Subscriber
from apps.prayer.schemas import PRAYER_NAMES


class City(models.Model):
    """Модель города."""

    link_to_csv = models.CharField(max_length=500, verbose_name="Ссылка для скачивания csv файла с временами намазов")
    name = models.CharField(max_length=200, verbose_name="Название городаk")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"{self.name} ({self.link_to_csv})"


class Day(models.Model):
    """Дата для намаза."""

    date = models.DateField(verbose_name="Дата намаза")

    class Meta:
        verbose_name = "Дата"
        verbose_name_plural = "Даты"

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")


class PrayerAtUserGroup(models.Model):
    """Модель для группировке намазов у пользователя."""

    pass


class Prayer(models.Model):
    """Модель намаза."""

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, verbose_name="Дата")
    time = models.TimeField(verbose_name="Время намаза")
    name = models.CharField(max_length=10, choices=PRAYER_NAMES, verbose_name="Название")

    class Meta:
        verbose_name = "Время намаза"
        verbose_name_plural = "Времена намазов"

    def __str__(self):
        return f"{self.city} {self.day} {self.time} {self.get_name_display()}"


class PrayerAtUser(models.Model):
    """Модель намаза для пользователя."""

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name="Подписчик")
    is_read = models.BooleanField(default=False, verbose_name="Прочитан ли намаз")
    prayer_group = models.ForeignKey(
        PrayerAtUserGroup, on_delete=models.CASCADE, verbose_name="Сгруппированные по 5 намазы для пользователя"
    )
    prayer = models.ForeignKey(
        Prayer, on_delete=models.CASCADE, verbose_name="", related_name="prayers_at_user"
    )

    class Meta:
        verbose_name = "Запись о намазе для пользователя"
        verbose_name_plural = "Записи о намазе для пользователей"

    def __str__(self):
        return f"{self.subscriber} {self.prayer}"

"""Базовые модели для работы с телеграмм."""
from django.conf import settings
from django.db import models

from bot_init.schemas import SUBSCRIBER_ACTIONS
from content.models import Ayat


class Mailing(models.Model):
    """Класс объеденяющий сообщения для удобного удаления при некорректной рассылке."""

    pass

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Mailing {self.pk}"


class AdminMessage(models.Model):
    """Административные сообщения."""

    title = models.CharField(max_length=128, verbose_name="Навзвание")
    text = models.TextField(verbose_name="Текст сообщения")
    key = models.CharField(max_length=128, verbose_name="Ключ, по которому сообщение вызывается в коде")

    class Meta:
        verbose_name = "Админитративное сообщение"
        verbose_name_plural = "Админитративное сообщения"

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    """Модель подписчика бота."""

    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    step = models.CharField(max_length=100, verbose_name="Шаг пользователя", blank=True)
    comment = models.TextField(blank=True, verbose_name="Комментарий к подписчику")
    day = models.IntegerField(default=2, verbose_name="День, для рассылки утреннего контента")
    favourite_ayats = models.ManyToManyField(
        Ayat, related_name="favorit_ayats", blank=True, verbose_name="Избранные аяты"
    )
    city = models.ForeignKey(
        "prayer.City", verbose_name="Город для рассылки намазов", on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return str(self.tg_chat_id)


class Admin(models.Model):
    """Модель администратора бота."""

    subscriber = models.OneToOneField(Subscriber, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return str(self.subscriber)


class Message(models.Model):
    """Модель для хранения сообщеинй."""

    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(blank=True, verbose_name="Текст сообщения")
    json = models.TextField()
    mailing = models.ForeignKey(Mailing, related_name="messages", on_delete=models.PROTECT, blank=True, null=True)
    is_unknown = models.BooleanField(default=False, verbose_name="Необработанное ли это сообщение")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        if self.from_user_id == settings.TG_BOT.id:
            return f"to {self.chat_id}"
        return f"from {self.chat_id}"

    def delete_in_tg(self):
        """Метод удаляет сообщение у пользователя в телеграмм."""
        from bot_init.service import delete_message_in_tg
        delete_message_in_tg(self.chat_id, self.message_id)
        return True


class SubscriberAction(models.Model):
    """Действие подписчика.

    Нужно для того, чтобы удобно вести статистику, отслеживаем 3 варианта событий:
     - Пользователь подписался
     - Пользователь отписался
     - Пользователь реактивировался

    """

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name="Подписчик")
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время")
    action = models.CharField(max_length=16, choices=SUBSCRIBER_ACTIONS, verbose_name="Действие")

    class Meta:
        verbose_name = "Действия пользователя"
        verbose_name_plural = "Действия пользователей"

    def __str__(self):
        return f"{self.subscriber} {self.action}"


class CallbackData(models.Model):
    """Модель для сохранения данных, с inline кнопок."""

    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    call_id = models.CharField(max_length=500, verbose_name="Идентификатор данных")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата из которого пришли данные")
    text = models.TextField(blank=True, verbose_name="Текст сообщения")
    json = models.TextField()

    class Meta:
        verbose_name = "Данные с inline кнопок"
        verbose_name_plural = "Данные с inline кнопок"

    def __str__(self):
        return f"{self.chat_id} {self.text}"

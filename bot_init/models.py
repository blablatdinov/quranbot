from django.db import models

from bot_init.schemas import SUBSCRIBER_ACTIONS
from content.models import Ayat


class Mailing(models.Model):
    pass


class AdminMessage(models.Model):
    """Административные сообщения"""
    title = models.CharField(max_length=128)
    text = models.TextField()
    key = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Админитративное сообщение'
        verbose_name_plural = 'Админитративное сообщения'


class Subscriber(models.Model):
    """ Модель подписчика бота """
    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика")
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(null=True)
    day = models.IntegerField(default=2)
    favorit_ayats = models.ManyToManyField(Ayat, related_name='favorit_ayats', blank=True, null=True)

    def __str__(self):
        return str(self.tg_chat_id)


    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Message(models.Model):
    """ Модель для хранения сообщеинй """
    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class SubscriberAction(models.Model):  # TODO подумать над именем класса
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=16, choices=SUBSCRIBER_ACTIONS)

    def __str__(self):
        return 'wow'


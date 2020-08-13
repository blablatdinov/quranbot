from django.db import models

from bot_init.schemas import SUBSCRIBER_ACTIONS
from content.models import Ayat


class Mailing(models.Model):
    """Класс объеденяющий сообщения для удобного удаления при некорректной рассылке"""
    pass


class AdminMessage(models.Model):
    """Административные сообщения"""
    title = models.CharField(max_length=128, verbose_name='Навзвание')
    text = models.TextField(verbose_name='Текст сообщения')
    key = models.CharField(max_length=128, verbose_name='Ключ, по которому сообщение вызывается в коде')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Админитративное сообщение'
        verbose_name_plural = 'Админитративное сообщения'


class Subscriber(models.Model):
    """ Модель подписчика бота """
    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к подписчику")
    day = models.IntegerField(default=2, verbose_name="День, для рассылки утреннего контента")
    favourite_ayats = models.ManyToManyField(
        Ayat, related_name='favorit_ayats', blank=True, verbose_name='Избранные аяты'
    )
    city = models.ForeignKey(
        'prayer.City', verbose_name='Город для рассылки намазов', on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return str(self.tg_chat_id)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Admin(models.Model):
    """Модель администратора бота"""
    subscriber = models.OneToOneField(Subscriber, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subscriber)

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"


class Message(models.Model):
    """ Модель для хранения сообщеинй """
    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()
    mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        if self.from_user_id == 705810219:
            return 'From bot'
        else:
            return 'To bot'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class SubscriberAction(models.Model):  # TODO подумать над именем класса
    """
    Действие подписчика

    Нужно для того, чтобы удобно вести статистику, отслеживаем 3 варианта событий:
     - Пользователь подписался
     - Пользователь отписался
     - Пользователь реактивировался

    """
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=16, choices=SUBSCRIBER_ACTIONS)

    def __str__(self):
        return f'{self.subscriber} {self.action}'

    class Meta:
        verbose_name = 'Действия пользователя'
        verbose_name_plural = 'Действия пользователей'


class CallbackData(models.Model):
    """Модель для сохранения данных, с inline кнопок"""
    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    call_id = models.CharField(max_length=500, verbose_name="Идентификатор данных")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата из которого пришли данные")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()

    def __str__(self):
        return f'{self.chat_id} {self.text}'

    class Meta:
        verbose_name = "Данные с inline кнопок"
        verbose_name_plural = "Данные с inline кнопок"

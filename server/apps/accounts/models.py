from typing import final

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


@final
class User(AbstractUser):
    """Модель пользователя."""

    chat_id = models.BigIntegerField(_('Telegram chat id'), primary_key=True)
    comment = models.TextField(blank=True, verbose_name=_('Comment for user'))
    day = models.IntegerField(default=2, verbose_name=_('Day for sending morning content'))
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta(object):
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

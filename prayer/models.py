from django.db import models

from bot_init.models import Subscriber


class PrayerGroup(models.Model):
    pass


class Prayer(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    prayer_group = models.ForeignKey(PrayerGroup, on_delete=models.CASCADE)

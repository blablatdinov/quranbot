from django.db import models

from bot_init.models import Subscriber
from prayer.schemas import PRAYER_NAMES


class City(models.Model):
    link_to_csv = models.CharField(max_length=500)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} ({self.link_to_csv})'


class Day(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')


class PrayerAtUserGroup(models.Model):
    pass


class Prayer(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time = models.TimeField()
    name = models.CharField(max_length=10, choices=PRAYER_NAMES)

    def __str__(self):
        return f'{self.city} {self.day} {self.time} {self.name}'


class PrayerAtUser(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    prayer_group = models.ForeignKey(PrayerAtUserGroup, on_delete=models.CASCADE)
    prayer = models.ForeignKey(Prayer, on_delete=models.CASCADE)

    def __str__(self):
        return ...

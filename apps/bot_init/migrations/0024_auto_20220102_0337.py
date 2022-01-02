# Generated by Django 3.2.10 on 2022-01-02 00:37
import ujson
from django.db import migrations


def update_message(apps, *args):
    Message = apps.get_model('bot', 'Message')
    for message in Message.objects.all():
        message.json = ujson.dumps(ujson.loads(message.json))
        message.save(update_fields=['json'])


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0023_auto_20211209_1546'),
    ]

    operations = [
    ]

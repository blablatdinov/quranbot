# Generated by Django 3.0.7 on 2020-07-28 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0002_auto_20200729_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='day',
            field=models.IntegerField(default=2),
        ),
    ]

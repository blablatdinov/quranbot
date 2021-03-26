# Generated by Django 3.1.7 on 2021-03-26 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0019_auto_20201219_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='referer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot_init.subscriber', verbose_name='Реферер подписчика'),
        ),
    ]

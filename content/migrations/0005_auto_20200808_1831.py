# Generated by Django 3.0.7 on 2020-08-08 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_remove_podcast_is_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayat',
            name='audio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile', verbose_name='Аудио файл'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='audio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile', verbose_name='Аудио файл'),
        ),
    ]

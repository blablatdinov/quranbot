# Generated by Django 3.0.7 on 2020-08-02 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ayat',
            name='content',
            field=models.TextField(default=1, verbose_name='Текст аята'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='audio_link',
            field=models.CharField(max_length=512, verbose_name='Ссылка на аудио'),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='tg_audio_link',
            field=models.CharField(max_length=512, verbose_name='Идентификатор файла в телеграмм'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='additional_content',
            field=models.TextField(blank=True, verbose_name='Допопнительный контент'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='arab_text',
            field=models.TextField(verbose_name='Арабский текст'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='audio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile', verbose_name='Аудио файл'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='ayat',
            field=models.CharField(max_length=16, verbose_name='Номер аята'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='html',
            field=models.TextField(verbose_name='Спарсенный HTML текст'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='link_to_source',
            field=models.CharField(max_length=512, verbose_name='Ссылка на источник'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='one_day_content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.MorningContent', verbose_name='Ежедневный контент'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='sura',
            field=models.IntegerField(verbose_name='Номер суры'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='trans',
            field=models.TextField(verbose_name='Транслитерация'),
        ),
        migrations.AlterField(
            model_name='morningcontent',
            name='additional_content',
            field=models.TextField(blank=True, verbose_name='Дополнительный текст'),
        ),
        migrations.AlterField(
            model_name='morningcontent',
            name='day',
            field=models.IntegerField(verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='audio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile', verbose_name='Аудио файл'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
    ]

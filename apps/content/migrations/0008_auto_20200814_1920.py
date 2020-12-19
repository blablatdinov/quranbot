# Generated by Django 3.0.7 on 2020-08-14 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20200808_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayat',
            name='arab_text',
            field=models.TextField(blank=True, verbose_name='Арабский текст'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='ayat',
            field=models.CharField(blank=True, max_length=16, verbose_name='Номер аята'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='content',
            field=models.TextField(blank=True, verbose_name='Текст аята'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='sura',
            field=models.IntegerField(blank=True, verbose_name='Номер суры'),
        ),
        migrations.AlterField(
            model_name='ayat',
            name='trans',
            field=models.TextField(blank=True, verbose_name='Транслитерация'),
        ),
    ]
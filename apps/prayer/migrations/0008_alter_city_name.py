# Generated by Django 3.2.10 on 2021-12-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0007_auto_20200823_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название города'),
        ),
    ]
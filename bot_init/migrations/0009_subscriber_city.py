# Generated by Django 3.0.7 on 2020-08-10 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0003_auto_20200810_1012'),
        ('bot_init', '0008_auto_20200808_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='prayer.City', verbose_name='Город для рассылки намазов'),
            preserve_default=False,
        ),
    ]

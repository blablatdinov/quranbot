# Generated by Django 3.0.7 on 2020-08-11 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0011_auto_20200811_1852'),
        ('prayer', '0005_auto_20200810_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='day',
            options={'verbose_name': 'Дата', 'verbose_name_plural': 'Даты'},
        ),
        migrations.AlterModelOptions(
            name='prayer',
            options={'verbose_name': 'Время намаза', 'verbose_name_plural': 'Времена намазов'},
        ),
        migrations.AlterModelOptions(
            name='prayeratuser',
            options={'verbose_name': 'Запись о намазе для пользователя', 'verbose_name_plural': 'Записи о намазе для пользователей'},
        ),
        migrations.AlterField(
            model_name='city',
            name='link_to_csv',
            field=models.CharField(max_length=500, verbose_name='Ссылка для скачивания csv файла с временами намазов'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название городаk'),
        ),
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(verbose_name='Дата намаза'),
        ),
        migrations.AlterField(
            model_name='prayer',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prayer.City', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='prayer',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prayer.Day', verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='prayer',
            name='name',
            field=models.CharField(choices=[('fajr', 'Иртәнге'), ('sunrise', 'Восход'), ('dhuhr', 'Өйлә'), ('asr', 'Икенде'), ('maghrib', 'Ахшам'), ("isha'a", 'Ястү')], max_length=10, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='prayer',
            name='time',
            field=models.TimeField(verbose_name='Время намаза'),
        ),
        migrations.AlterField(
            model_name='prayeratuser',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Прочитан ли намаз'),
        ),
        migrations.AlterField(
            model_name='prayeratuser',
            name='prayer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prayer.Prayer', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='prayeratuser',
            name='prayer_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prayer.PrayerAtUserGroup', verbose_name='Сгруппированные по 5 намазы для пользователя'),
        ),
        migrations.AlterField(
            model_name='prayeratuser',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_init.Subscriber', verbose_name='Подписчик'),
        ),
    ]
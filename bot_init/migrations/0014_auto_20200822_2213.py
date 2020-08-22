# Generated by Django 3.0.9 on 2020-08-22 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0013_auto_20200812_0932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterField(
            model_name='subscriberaction',
            name='action',
            field=models.CharField(choices=[('subscribed', 'подписался'), ('unsubscribed', 'отписался'), ('reactivated', 'реактивировался')], max_length=16, verbose_name='Действие'),
        ),
        migrations.AlterField(
            model_name='subscriberaction',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата/время'),
        ),
        migrations.AlterField(
            model_name='subscriberaction',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_init.Subscriber', verbose_name='Подписчик'),
        ),
    ]

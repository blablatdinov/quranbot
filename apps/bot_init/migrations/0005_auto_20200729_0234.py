# Generated by Django 3.0.7 on 2020-07-28 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0004_subscriberaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriberaction',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_init.Subscriber'),
        ),
    ]
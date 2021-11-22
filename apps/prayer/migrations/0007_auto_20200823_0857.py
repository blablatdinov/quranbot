# Generated by Django 3.0.7 on 2020-08-23 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0006_auto_20200811_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prayeratuser',
            name='prayer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prayers_at_user', to='prayer.Prayer', verbose_name=''),
        ),
    ]

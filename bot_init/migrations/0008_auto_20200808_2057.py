# Generated by Django 3.0.7 on 2020-08-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0007_auto_20200805_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к подписчику'),
        ),
    ]

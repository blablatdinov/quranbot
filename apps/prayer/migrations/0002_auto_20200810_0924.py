# Generated by Django 3.0.7 on 2020-08-10 06:24

from django.db import migrations


def add_kazan(apps, schema_editor):
    City = apps.get_model('prayer', 'City')
    City.objects.create(name='kazan', link_to_csv='http://dumrt.ru/netcat_files/391/638/Kazan.csv')


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_kazan),
    ]
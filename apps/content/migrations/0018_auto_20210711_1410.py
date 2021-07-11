# Generated by Django 3.2.4 on 2021-07-11 11:10

from django.db import migrations
from apps.content.services.get_content_from_morning_content import get_content


def delete_too_many_len_content(apps, schema_editor):
    MorningContent = apps.get_model('content', 'MorningContent')
    for m in MorningContent.objects.all():
        if len(get_content(m.ayat_set.all(), m.additional_content)) > 4096:
            MorningContent.objects.filter(pk__gte=m.pk).delete()

def delete_morning_content_without_body(apps, schema_editor):
    MorningContent = apps.get_model('content', 'MorningContent')
    for m in MorningContent.objects.all():
        if m.ayat_set.count == 0:
            m.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_auto_20210409_2109'),
    ]

    operations = [
        migrations.RunPython(delete_morning_content_without_body),
        migrations.RunPython(delete_too_many_len_content),
    ]

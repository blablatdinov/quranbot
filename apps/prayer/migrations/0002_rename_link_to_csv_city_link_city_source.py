# Generated by Django 4.0 on 2022-01-02 12:31

from django.db import migrations, models


def set_source(apps, *args):
    City = apps.get_model('prayer', 'City')
    City.objects.all().update(source='DUM_RT')
    City.objects.filter(name='Москва').update(source='TIME_NAMAZ')
    City.objects.filter(name='Уфа').update(source='TIME_NAMAZ')


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0001_initial_squashed_0009_auto_20220102_0426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='link_to_csv',
            new_name='link',
        ),
        migrations.AddField(
            model_name='city',
            name='source',
            field=models.CharField(choices=[('DUM_RT', 'Дум РТ (http://dumrt.ru/)'), ('TIME_NAMAZ', 'Сайт https://time-namaz.ru')], default=1, max_length=16, verbose_name='Источник для парсинга намазов'),
            preserve_default=False,
        ),
        migrations.RunPython(set_source),
    ]
# Generated by Django 3.0.7 on 2020-07-28 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_link', models.CharField(max_length=512)),
                ('tg_audio_link', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='MorningContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_content', models.TextField(blank=True)),
                ('day', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Ежедневный контент для пользователей',
                'verbose_name_plural': 'Ежедневный контент для пользователей',
            },
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('is_flag', models.BooleanField(default=False, verbose_name='Последнее аудио за сессию парсинга')),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile')),
            ],
            options={
                'verbose_name': 'Аудио подкаст',
                'verbose_name_plural': 'Аудио подкасты',
            },
        ),
        migrations.CreateModel(
            name='Ayat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_content', models.TextField(blank=True)),
                ('arab_text', models.TextField()),
                ('trans', models.TextField()),
                ('sura', models.IntegerField()),
                ('ayat', models.CharField(max_length=16)),
                ('html', models.TextField()),
                ('link_to_source', models.CharField(max_length=512)),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.AudioFile')),
                ('one_day_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.MorningContent')),
            ],
            options={
                'verbose_name': 'Аят Священного Корана',
                'verbose_name_plural': 'Аяты Священного Корана',
            },
        ),
    ]

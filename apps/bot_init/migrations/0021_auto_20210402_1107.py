# Generated by Django 3.1.7 on 2021-04-02 08:07

from django.db import migrations


def create_concourse_admin_message(apps, schema_editor):
    AdminMessage = apps.get_model("bot_init", "AdminMessage")

    AdminMessage.objects.create(
        text=""" 💥Розыгрыш💥

Наступает священный месяц Рамадан и я хочу разыграть среди своих пользователей бота 3 дневника помощника📿

Этот дневник вы могли увидеть на Инстаграмм-странице моей жены <a href="https://www.instagram.com/a.agush/">a.agush</a>

Такого дневника НИГДЕ нет, это ограниченный товар, его нигде нельзя купить. Поэтому у вас есть возможность выиграть его для себя или своей жены/сестры/подруги.

 Условия:

1️⃣ Быть подписчиком бота @Quran_365_bot
2️⃣ Получить реферальную ссылку, нажав на кнопку «»
3️⃣ Пригласить как минимум 1 друга подписаться на @Quran_365_bot по своей реферальной ссылке.

Результаты узнаем 8 апреля в 20:00 по МСК с помощью рандомайзера🎲

Участвуют все города России, доставка за мой счёт🚛 """,
        key="concourse",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0020_subscriber_referer'),
    ]

    operations = [
        migrations.RunPython(create_concourse_admin_message)
    ]

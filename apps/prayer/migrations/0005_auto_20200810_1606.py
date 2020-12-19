# Generated by Django 3.0.7 on 2020-08-10 13:06

from django.db import migrations
from django.db.migrations import RunPython


def write_cities(apps, schema_editor):
    City = apps.get_model('prayer', 'City')
    a = [
        '/netcat_files/391/638/Agriz.csv Агрыз',
        '/netcat_files/391/638/Aznakay.csv Азнакаево',
        '/netcat_files/391/638/Aksubay.csv Аксубаево',
        '/netcat_files/391/638/Aktanis.csv Актаныш',
        '/netcat_files/391/638/Aleksey.csv Алексеевск',
        '/netcat_files/391/638/Almet.csv Альметьевск',
        '/netcat_files/391/638/Apastovo.csv Апастово',
        '/netcat_files/391/638/Arsk.csv Арск',
        '/netcat_files/391/638/Bavli.csv Бавлы',
        '/netcat_files/391/638/BazarnyeMataki.csv Базарные Матаки',
        '/netcat_files/391/638/Baltasi.csv Балтаси',
        '/netcat_files/391/638/BogatyeSaby.csv Богатые Сабы',
        '/netcat_files/391/638/Bolgary.csv Болгар',
        '/netcat_files/391/638/BolshAtna.csv Большая Атня',
        '/netcat_files/391/638/BolshieKaybesy.csv Большие Кайбицы',
        '/netcat_files/391/638/Bugulma.csv Бугульма',
        '/netcat_files/391/638/Buinsk.csv Буинск',
        '/netcat_files/391/638/VerhUslon.csv Верхний Услон',
        '/netcat_files/391/638/VicokayGora.csv Высокая Гора',
        '/netcat_files/391/638/Elabuga.csv Елабуга',
        '/netcat_files/391/638/Zainsk.csv Заинск',
        '/netcat_files/391/638/Zelenodolsk.csv Зеленодольск',
        '/netcat_files/391/638/Kazan.csv Казань',
        '/netcat_files/391/638/KamskoeUstye.csv Камское Устье',
        '/netcat_files/391/638/Kukmor.csv Кукмор',
        '/netcat_files/391/638/Laish.csv Лаишево',
        '/netcat_files/391/638/Leninogorsk.csv Лениногорск',
        '/netcat_files/391/638/Mamadis.csv Мамадыш',
        '/netcat_files/391/638/Mendeleevsk.csv Менделеевск',
        '/netcat_files/391/638/Menzilinsk.csv Мензелинск',
        '/netcat_files/391/638/Muslimov.csv Муслюмово',
        '/netcat_files/391/638/NabChelny.csv Набережные Челны',
        '/netcat_files/391/638/Nignekamsk.csv Нижнекамск',
        '/netcat_files/391/638/Novosesminsk.csv Новошешминск',
        '/netcat_files/391/638/Nurlat.csv Нурлат',
        '/netcat_files/391/638/Pestrezy.csv Пестрецы',
        '/netcat_files/391/638/RibnayaSlpboda.csv Рыбная Слобода',
        '/netcat_files/391/638/Sarmanovo2.csv Сарманово',
        '/netcat_files/391/638/StaroeChuprale.csv Старое Дрожжаное',
        '/netcat_files/391/638/Tet2.csv Тетюши',
        '/netcat_files/391/638/Tulyachi.csv Тюлячи',
        '/netcat_files/391/638/Urussu.csv Уруссу',
        '/netcat_files/391/638/Cheremsan.csv Черемшан',
        '/netcat_files/391/638/Chistop.csv Чистополь',
    ]
    for elem in a:
        short_link, city = elem.split('v ')
        City.objects.create(link_to_csv=f'http://dumrt.ru{short_link}v', name=city)


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0004_auto_20200810_1557'),
    ]

    operations = [
        migrations.RunPython(write_cities)
    ]
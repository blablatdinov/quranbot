from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'quranbot.blablatdinov.ru',
    'quranbot.blablatdinov.ru:80',
    '66.55.70.132',
    '66.55.70.132:80',
]

SECRET_KEY = '=sz@3fkwt!=mnfkl(he+b0neftn*9qc69vv38q2q*s54)vhmz!'


DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quranbot_db',
        'USER': 'quranbot_user',
        'PASSWORD': 'quranbot_user',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = '/home/www/code/quranbot/static'

TG_BOT_TOKEN = '705810219:AAHwIwmLT7P3ffdP5fV6OFy2kWvBSDERGNk'




DJANGO_TELEGRAMBOT = {
    'WEBHOOK_SITE': 'https://quranbot.blablatdinov.ru',
    'BOTS': [
        {
            'TOKEN': TG_BOT_TOKEN
        },
    ],
}

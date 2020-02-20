from .base import *

DEBUG = False


ALLOWED_HOSTS = [
    'blablatdinov.ru',
    'blablatdinov.ru:80',
    '66.55.70.132:80',
    '66.55.70.132',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'quranbot_db',
        #'USER': 'quranbot_user',
        #'PASSWORD': 'quranbot_user',
        #'HOST': 'localhost',
        #'PORT': '',
    }
}

DJANGO_TELEGRAMBOT = {
    'WEBHOOK_SITE': 'https://blablatdinov.ru',
    'BOTS': [
        {
            'TOKEN': '705810219:AAHwIwmLT7P3ffdP5fV6OFy2kWvBSDERGNk'
        },
    ],

}

STATIC_ROOT = '/home/www/code/quranbot/static'

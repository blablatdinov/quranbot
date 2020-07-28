from .base import *

from dotenv import load_dotenv


project_folder = BASE_DIR
load_dotenv(os.path.join(project_folder, '.env'))

DEBUG = True

ALLOWED_HOSTS = [
    'quranbot.blablatdinov.ru',
    'quranbot.blablatdinov.ru:80',
    'blablatdinov.ru:80',
    'blablatdinov.ru'
]

SECRET_KEY = '=sz@3fkwt!=mnfkl(he+b0neftn*9qc69vv38q2q*s54)vhmz!'


DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('qbot_db_name'),
        'USER': os.getenv('qbot_db_username'),
        'PASSWORD': os.getenv('qbot_db_password'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = '/home/www/code/quranbot/static'

TG_BOT_TOKEN = os.getenv('qbot_tg_token')


DJANGO_TELEGRAMBOT = {
    'WEBHOOK_SITE': 'https://quranbot.blablatdinov.ru',
    'BOTS': [
        {
            'TOKEN': TG_BOT_TOKEN
        },
    ],
}

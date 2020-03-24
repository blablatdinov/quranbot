from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

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

TG_BOT_TOKEN = '452230948:AAGgl86AHCdTCXf8XGD6lkj9rQhoV4xrf5E'



DJANGO_TELEGRAMBOT = {
    'WEBHOOK_SITE': 'https://ac48c51a.ngrok.io',
    'BOTS': [
        {
            'TOKEN': TG_BOT_TOKEN
        },
    ],
}

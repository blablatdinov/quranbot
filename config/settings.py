import os
from collections import namedtuple

from dotenv import load_dotenv
import requests


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv('.env')

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bot_init',
    'content',
    'prayer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id', 'admins'])
TG_BOT.token = os.getenv('BOT_TOKEN')
TG_BOT.webhook_host = os.getenv('HOST')
r = requests.get(f'https://api.telegram.org/bot{TG_BOT.token}/getMe').json()
if not r.get('ok'):
    print(r)  # TODO Нормальное логгирование
    exit()
try:
    if os.getenv('ADMINS') == '':
        TG_BOT.admins = []
    else:
        TG_BOT.admins = [int(chat_id) for chat_id in os.getenv('ADMINS').split(',')]
except ValueError:
    print('Пожалуйста проверьте переменную ADMINS в файле .env')
    exit()
except AttributeError:
    print('Пожалуйста проверьте переменную ADMINS в файле .env')
    exit()
TG_BOT.name = r['result']['username']
TG_BOT.id = r['result']['id']

CELERY_BROKER_URL = 'redis://localhost:6379/1'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASKS_SERIALIZER = 'json'
#
#
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
#
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

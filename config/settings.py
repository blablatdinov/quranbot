import os
from collections import namedtuple

import ddtrace
import toml
from loguru import logger
from split_settings.tools import include

from config.splitted_settings.environ import env

include(
    'splitted_settings/boilerplate.py',
    'splitted_settings/db.py',
    'splitted_settings/installed_apps.py',
    'splitted_settings/static.py',
    'splitted_settings/templates.py',
    'splitted_settings/rest_framework.py',
    'splitted_settings/logger.py',
    'splitted_settings/middlewares.py',
    'splitted_settings/templates.py',
    'splitted_settings/cors.py',
)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', list)
HOST = env('HOST', str)

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

USE_TZ = True

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id', 'admins'])
TG_BOT.token = os.getenv('BOT_TOKEN')
TG_BOT.webhook_host = os.getenv('HOST')
try:
    if os.getenv('ADMINS') == '':
        TG_BOT.admins = []
    else:
        TG_BOT.admins = [int(chat_id) for chat_id in os.getenv('ADMINS').split(',')]
except ValueError as e:
    logger.error('Пожалуйста проверьте переменную ADMINS в файле .env')
    raise e
except AttributeError as e:
    logger.error('Пожалуйста проверьте переменную ADMINS в файле .env')
    raise e
TG_BOT.name = os.getenv('BOT_NAME', 'Quran_365_bot')
TG_BOT.id = os.getenv('BOT_ID', '705810219')

CELERY_BROKER_URL = os.getenv('REDIS_CONNECTION')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASKS_SERIALIZER = 'json'
print(ALLOWED_HOSTS)

if DEBUG:  # noqa: F821
    ddtrace.tracer.enabled = not DEBUG  # noqa: F821
    ddtrace.patch_all()

RAMADAN_MODE = env('RAMADAN_MODE', bool, default=False)

with open(f'{BASE_DIR}/pyproject.toml', 'r') as f:  # noqa: F821
    PYPROJECT_FILE = toml.loads(f.read())

VERSION = PYPROJECT_FILE['tool']['poetry']['version']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENABLE_S3 = env('ENABLE_S3', bool, default=False)

CSRF_TRUSTED_ORIGINS = ['https://quranbot.blablatdinov.ru']

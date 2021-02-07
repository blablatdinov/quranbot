import os
from collections import namedtuple

from dotenv import load_dotenv
import requests
from loguru import logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "apps.api",
    "apps.bot_init",
    "apps.content",
    "apps.prayer"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "static/"

TG_BOT = namedtuple("Bot", ["token", "webhook_host", "name", "id", "admins"])
TG_BOT.token = os.getenv("BOT_TOKEN")
TG_BOT.webhook_host = os.getenv("HOST")
r = requests.get(f"https://api.telegram.org/bot{TG_BOT.token}/getMe").json()
if not r.get("ok"):
    logger.info(r)
    exit(1)
try:
    if os.getenv("ADMINS") == "":
        TG_BOT.admins = []
    else:
        TG_BOT.admins = [int(chat_id) for chat_id in os.getenv("ADMINS").split(",")]
except ValueError as e:
    logger.error("Пожалуйста проверьте переменную ADMINS в файле .env")
    raise e
except AttributeError as e:
    logger.error("Пожалуйста проверьте переменную ADMINS в файле .env")
    raise e
TG_BOT.name = r["result"]["username"]
TG_BOT.id = r["result"]["id"]

CELERY_BROKER_URL = os.getenv("REDIS_CONNECTION")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASKS_SERIALIZER = "json"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
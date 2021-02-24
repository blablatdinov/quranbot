import os
from collections import namedtuple

from dotenv import load_dotenv
import requests
from loguru import logger
from split_settings.tools import include

from config.splitted_settings.environ import env

DEBUG = env("DEBUG")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

include(
    "splitted_settings/boilerplate.py",
    "splitted_settings/db.py",
    "splitted_settings/installed_apps.py",
    "splitted_settings/static.py",
    "splitted_settings/templates.py",
    "splitted_settings/rest_framework.py",
)

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
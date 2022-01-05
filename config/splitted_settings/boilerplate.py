import os.path

from config.splitted_settings.environ import env

DEBUG = env('DEBUG')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'config.urls'

SECRET_KEY = env('SECRET_KEY')

# Disable built-in ./manage.py test command in favor of pytest

WSGI_APPLICATION = 'config.wsgi.application'

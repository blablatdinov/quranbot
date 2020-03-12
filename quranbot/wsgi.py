"""
WSGI config for quranbot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quranbot.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quranbot.settings.prod')


application = get_wsgi_application()

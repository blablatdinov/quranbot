import os

from django.core.wsgi import get_wsgi_application


using_settings = 'config.settings.prod'
os.environ['DJANGO_SETTINGS_MODULE'] = using_settings

application = get_wsgi_application()

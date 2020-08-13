import os

from django.core.wsgi import get_wsgi_application


if os.getenv('DEBUG') == 'true':
    using_settings = 'config.settings.dev'
else:
    using_settings = 'config.settings.prod'
os.environ['DJANGO_SETTINGS_MODULE'] = using_settings

application = get_wsgi_application()

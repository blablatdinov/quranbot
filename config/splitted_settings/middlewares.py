from django.http import HttpResponse
from loguru import logger
import traceback

from config.splitted_settings.boilerplate import DEBUG


class DebugErrorMiddleware():

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        print(traceback.format_exc())
        return HttpResponse(traceback.format_exc().replace('\n', '<br>'), status=500)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['config.splitted_settings.middlewares.DebugErrorMiddleware']

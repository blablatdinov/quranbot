import traceback
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse
from loguru import logger

from config.splitted_settings.boilerplate import DEBUG


class DebugErrorMiddleware:

    def __init__(self, get_response: Callable) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        return self._get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        logger.error(traceback.format_exc())
        return HttpResponse(traceback.format_exc().replace('\n', '<br>'), status=500)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_extensions',
]

if DEBUG:
    MIDDLEWARE += ['config.splitted_settings.middlewares.DebugErrorMiddleware']

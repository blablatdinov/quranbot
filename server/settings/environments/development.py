"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!

The MIT License (MIT).

Copyright (c) 2018-2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import socket

from server.settings.components import config
from server.settings.components.common import DATABASES, INSTALLED_APPS, MIDDLEWARE

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = [
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]


# Installed apps for development only:

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',
    'nplusone.ext.django',

    # Linting migrations:
    'django_migration_linter',

    # django-test-migrations:
    'django_test_migrations.contrib.django_checks.AutoNames',
    # This check might be useful in production as well,
    # so it might be a good idea to move `django-test-migrations`
    # to prod dependencies and use this check in the main `settings.py`.
    # This will check that your database is configured properly,
    # when you run `python manage.py check` before deploy.
    'django_test_migrations.contrib.django_checks.DatabaseConfiguration',

    # django-extra-checks:
    'extra_checks',
)


# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{0}.1'.format(ip[:ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']


def _custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':
        'server.settings.environments.development._custom_show_toolbar',
}

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_SCRIPT_SRC = ("'self'", 'ajax.googleapis.com')
CSP_IMG_SRC = ("'self'", 'data:')
CSP_CONNECT_SRC = ("'self'",)


# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = (  # noqa: WPS440
    'nplusone.ext.django.NPlusOneMiddleware',
) + MIDDLEWARE

# Logging N+1 requests:
NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger('django')
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {'model': 'admin.*'},
]


# django-test-migrations
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
DTM_IGNORED_MIGRATIONS = frozenset((
    ('axes', '*'),
))


# django-extra-checks
# https://github.com/kalekseev/django-extra-checks

EXTRA_CHECKS = {
    'checks': [
        # Forbid `unique_together`:
        'no-unique-together',
        # Use the indexes option instead:
        'no-index-together',
        # Each model must be registered in admin:
        'model-admin',
        # FileField/ImageField must have non empty `upload_to` argument:
        'field-file-upload-to',
        # Text fields shouldn't use `null=True`:
        'field-text-null',
        # Prefer using BooleanField(null=True) instead of NullBooleanField:
        'field-boolean-null',
        # Don't pass `null=False` to model fields (this is django default)
        'field-null',
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {'id': 'field-foreign-key-db-index', 'when': 'indexes'},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        'field-default-null',
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        'field-choices-constraint',
    ],
}

# Disable persistent DB connections
# https://docs.djangoproject.com/en/3.2/ref/databases/#caveats
DATABASES['default']['CONN_MAX_AGE'] = 0

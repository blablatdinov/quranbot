import os


if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    from quranbot.settings.dev import *
else:
    from quranbot.settings.prod import *

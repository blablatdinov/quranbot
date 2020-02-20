from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if DEBUG:
    TOKEN = '452230948:AAGgl86AHCdTCXf8XGD6lkj9rQhoV4xrf5E'
else:
    TOKEN = '705810219:AAHwIwmLT7P3ffdP5fV6OFy2kWvBSDERGNk'

DJANGO_TELEGRAMBOT = {
    # 'WEBHOOK_SITE': input('Please enter address for webhook: '),
    'WEBHOOK_SITE': '',
    'BOTS': [
        {
            'TOKEN': TOKEN
        },
    ],

}

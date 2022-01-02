from config.splitted_settings.boilerplate import DEBUG
from config.splitted_settings.environ import env

ALLOWED_HOSTS = [env('HOST').replace('http://', '').replace('https://', '')]

if DEBUG:
    ALLOWED_HOSTS += ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from config.splitted_settings.environ import env

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}
print(DATABASES)

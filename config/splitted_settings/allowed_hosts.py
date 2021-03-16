from config.splitted_settings.environ import env

ALLOWED_HOSTS = [env("HOST")]

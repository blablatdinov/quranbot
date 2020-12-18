#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv


load_dotenv(".env")


def main():
    """Главная функция работы с django-cli."""
    if os.getenv("DEBUG") == "true":
        using_settings = "config.settings.dev"
    else:
        using_settings = "config.settings.prod"
    os.environ["DJANGO_SETTINGS_MODULE"] = using_settings
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

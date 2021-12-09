from django.conf import settings


def test():
    assert settings.VERSION != ''
    assert settings.VERSION is not None

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def mixer():
    from mixer.backend.django import mixer
    return mixer


@pytest.fixture()
def anon():
    return APIClient()


@pytest.fixture()
def user(mixer):
    return mixer.blend(User)


@pytest.fixture()
def client(anon, user):
    anon.force_authenticate(user=user)
    return anon


"""
FAILED tests/api/test_get_data_for_usage_graphic.py::test - Assertio...
FAILED tests/api/test_get_ping_to_message.py::test - AssertionError:...
FAILED tests/api/content/test_get_ayats_which_not_used_in_morning_content.py::test
"""

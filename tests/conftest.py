import pytest
import requests_mock
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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


@pytest.fixture()
def http_mock():
    with requests_mock.Mocker() as m:
        yield m





"""
FAILED tests/bot_init/test_start_message_controller.py::test_start_message_with_referal_service
"""

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

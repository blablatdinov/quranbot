import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import RequestsClient

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture()
def user(mixer):
    user = mixer.blend(User)
    user.set_password('asdf')
    user.save()
    return user


def test_get_token(anon, user):
    got = anon.post('/api/v1/token/', data={
        'username': user.username,
        'password': 'asdf',
    })

    assert list(got.json().keys()) == ['refresh', 'access']


def test_auth_by_token(anon, user):
    token = anon.post('/api/v1/token/', data={
        'username': user.username,
        'password': 'asdf',
    }).json()['access']
    # Authorzation: Bearer <token>
    anon.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    got = anon.get('/api/v1/ayats/')

    assert got.status_code == 200

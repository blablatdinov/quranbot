import pytest
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture()
def user(mixer):
    user = mixer.blend(User)
    user.set_password('asdf')
    user.save()
    return user


def test_get_token(anon, user):
    print(User.objects.all())
    got = anon.post('/api/v1/token/', data={
        'username': user.username,
        'password': 'asdf',
    })

    assert list(got.json().keys()) == ['refresh', 'access']

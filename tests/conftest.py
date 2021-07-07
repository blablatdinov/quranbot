import pytest


@pytest.fixture()
def mixer():
    from mixer.backend.django import mixer
    return mixer

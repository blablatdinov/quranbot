import pytest

from apps.content.service import format_count_to_text

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('number,text', [
    (1, 'аят'),
    (20, 'аятов'),
    (2, 'аята'),
    (5, 'аятов'),
    (11, 'аятов'),
    (21, 'аят'),
    (17, 'аятов'),
    (178, 'аятов'),
    (53, 'аята'),
])
def test_format_ayats_count(number, text):
    got = format_count_to_text(number)
    assert got == text

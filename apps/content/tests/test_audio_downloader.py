import pytest
from apps.content.services.parse_and_download_audios_for_ayat import format_num


@pytest.mark.parametrize("num,expected_value", [
    ("9", "009"),
    ("2", "002"),
    ("74", "074"),
    ("114", "114"),

    ("1-5", "001-5"),
    ("55-66", "055-66"),
    ("55, 66", "055-66"),
])
def test_format_num(num, expected_value):
    got = format_num(num)

    assert got == expected_value
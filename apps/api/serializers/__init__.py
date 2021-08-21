from .ayat_serializer import AyatSerializer, AyatListSerializer  # noqa
from .morning_content_serializer import MorningContentSerializer, MorningContentCreateSerializer  # noqa
from .mailing_serializer import MailingSerializer, MailingCreateSerializer

__all__ = [
    AyatSerializer,
    AyatListSerializer,
    MorningContentSerializer,
    MorningContentCreateSerializer,
    MailingSerializer,
    MailingCreateSerializer,
]

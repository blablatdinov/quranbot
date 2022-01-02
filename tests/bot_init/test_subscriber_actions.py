import pytest

from apps.bot_init.models import SubscriberAction
from apps.bot_init.service import (
    _created_subscriber_service,
    _not_created_subscriber_service,
    _subscriber_unsubscribed,
    get_admins_list,
)
from apps.bot_init.services.answer_service import Answer, AnswersList

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def deactivated_subscriber(subscriber):
    subscriber.is_active = False
    subscriber.save()
    return subscriber


def test_new_subscriber_services(subscriber, morning_content):
    got = _created_subscriber_service(subscriber)

    assert type(got) is AnswersList
    assert len(got) == 2 + len(get_admins_list())
    assert list(set([x.chat_id for x in got[:2]]))[0] == subscriber.tg_chat_id
    assert SubscriberAction.objects.count() == 1
    assert SubscriberAction.objects.last().action == 'subscribed'


def test_not_created_subscriber_service(subscriber):
    got = _not_created_subscriber_service(subscriber)

    assert type(got) is Answer
    assert got.text == 'Вы уже зарегистрированы'


def test_subscriber_unsubscribed(subscriber):
    _subscriber_unsubscribed(subscriber.tg_chat_id)

    assert SubscriberAction.objects.count() == 1
    assert SubscriberAction.objects.last().action == 'unsubscribed'


def test_subscriber_reactivation(deactivated_subscriber):
    got = _not_created_subscriber_service(deactivated_subscriber)

    assert got.text == 'Рады видеть вас снова, вы продолжите с дня 2'
    assert SubscriberAction.objects.count() == 1
    assert SubscriberAction.objects.last().action == 'reactivated'

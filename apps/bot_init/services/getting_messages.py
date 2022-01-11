from django.db.models import Q, QuerySet

from apps.bot_init.models import Message


def get_messages(search_param: str = None, in_mailing: bool = False, is_unknown: bool = False) -> QuerySet[Message]:
    if not in_mailing and not is_unknown:
        return Message.objects.all()

    q = Q()
    if is_unknown:
        is_unknown = is_unknown == 'true'
        q = q | Q(is_unknown=is_unknown)

    if in_mailing:
        in_mailing = in_mailing == 'true'
        q = q | Q(mailing__isnull=not in_mailing)

    if search_param:
        q = q | Q(text=search_param) | Q(from_user_id=search_param) | Q(chat_id=search_param)

    return Message.objects.filter(q)

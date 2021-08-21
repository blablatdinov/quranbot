from rest_framework.exceptions import APIException


class ChatIdOrCityNotGived(APIException):
    status_code = 412
    default_detail = 'Передайте chat_id или город.'


class SubscriberNotDefinedCityAPIException(APIException):
    status_code = 412
    default_detail = 'Пользователь не определил город.'

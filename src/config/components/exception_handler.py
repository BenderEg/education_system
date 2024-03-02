from http import HTTPStatus

from django.http import JsonResponse

from config.base_error import BaseError


def custom_exception_handler(exc: Exception, context):
    if isinstance(exc, BaseError):
        return JsonResponse(data=exc.get_message(), status=exc.status_code)
    return JsonResponse(data={"detail": exc.args},
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)

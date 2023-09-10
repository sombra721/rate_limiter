import pytz

from datetime import datetime
from http import HTTPStatus

from django.http import JsonResponse

from .utils.rate_limiter import rate_limiter_dec


@rate_limiter_dec
def index(request):
    # Current only accept GET method, return 405 http status code for other method
    if request.method != "GET":
        data_dict = {'status': 'false',
                     'message': f"{request.method} method is not allowed, only GET method is accepted."}
        return JsonResponse(data_dict, status=HTTPStatus.METHOD_NOT_ALLOWED)

    # return the current time with timezone information in JSON
    if "TZ" in request.META and request.META["TZ"]:
        timezone = pytz.timezone(request.META["TZ"])
    else:
        timezone = pytz.timezone("UTC")
    current_time = datetime.now(timezone).strftime("%Y/%m/%d %H:%M:%S %Z")
    data_dict = {'status': 'true', 'message': f"Current time: {current_time}"}

    return JsonResponse(data_dict, status=HTTPStatus.OK)

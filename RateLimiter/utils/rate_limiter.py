from collections import deque
from datetime import datetime
from http import HTTPStatus

from django.http import JsonResponse
from django.conf import settings


class RateLimiter:

    def __init__(self):
        self.request_limit = settings.REQUEST_LIMIT
        self.time_range = settings.TIME_RANGE
        self.user_request_timestamp = {}


rate_limiter = RateLimiter()


def rate_limiter_dec(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        user_ip = args[0].META.get('REMOTE_ADDR')
        now = datetime.utcnow().timestamp() * 1000.0

        # if the user already made request(s)
        if user_ip in rate_limiter.user_request_timestamp:
            # remove the previous requests which made longer than the time range defined
            while rate_limiter.user_request_timestamp[user_ip] and \
                    now - rate_limiter.user_request_timestamp[user_ip][0] > rate_limiter.time_range:
                rate_limiter.user_request_timestamp[user_ip].popleft()

            # if the number of requests within the time period, append the timestamp into the queue.
            if len(rate_limiter.user_request_timestamp[user_ip]) < rate_limiter.request_limit:
                rate_limiter.user_request_timestamp[user_ip].append(now)
            # Number of requests exceeds the limitation, return 429 http status code too many request.
            else:
                data_dict = {
                    'status': 'false',
                    'message': f'There are too many requests in a given amount of time '
                               f'({rate_limiter.request_limit} requests in past {rate_limiter.time_range} milliseconds)'}
                return JsonResponse(data_dict, status=HTTPStatus.TOO_MANY_REQUESTS)
        # User has not made any requests yet, initiate a new queue to store the timestamp when user made the request.
        else:
            rate_limiter.user_request_timestamp[user_ip] = deque()
            rate_limiter.user_request_timestamp[user_ip].append(now)

        # Response the original result from the method
        return result

    return wrapper

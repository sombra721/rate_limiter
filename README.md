# Rate Limiter for Django Applications

Simple program that returns the current time with limiting the number of requests from a user in defined time range.

A class (`RateLimiter`) is created to store the rate limiter data.

Using a decorator function (`rate_limiter_dec`) which could be used by other functions in `views.py`.
Before executing the method in views, check if the number of requests has exceeds the rate limitation.


## Getting started

Add below variables in the settings.py:

1. TIME_RANGE: Time frame (millisecond) that limits the number of requests a user can make within it.
2. REQUEST_LIMIT: Number of requests a user can make within  the time frame.

## Usage

Use the decorator for the function(s) in `views.py`:
```
@rate_limiter_dec
def index(request):
    ...
```

Start the server with below command:
```
python manage.py runserver
```

## Results

If we set time frame with 3 seconds (3000 millisecond) and number of request 5
```
# Time range for rate limiter in millisecond
TIME_RANGE = 3000

# Number of request allowed within the time period
REQUEST_LIMIT = 5
```

Case 1: If the request is not with GET method
```
http status code: 405
{
  "status": "false",
  "message": "POST method is not allowed, only GET method is accepted."
}
```

Case 2: If the number of requests the user made exceeds the rate limitation
```
http status code: 429
{
  "status": "false",
  "message": "There are too many requests in a given amount of time (5 requests in past 3000 milliseconds)"
}
```

Case 3: If the number of requests the user made does not exceed the rate limitation
```
http status code: 200
{
  "status": "true",
  "message": "Current time: 2023/09/08 23:31:19 UTC"
}
```
# Rate Limiter for Django Applications

Simple program that returns the current time with limiting the number of requests from a user in defined time range.

A class [rate_limiter.py](https://github.com/sombra721/rate_limiter/blob/main/RateLimiter/utils/rate_limiter.py) is created to store the rate limiter data.

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

Start the server with the below command:
```
python manage.py runserver
```

## Results

If we set time frame with 3 seconds (3000 millisecond) and the limitation of 5 request within the time frame.

```
# Time range for rate limiter in millisecond
TIME_RANGE = 3000

# Number of request allowed within the time period
REQUEST_LIMIT = 5
```

Sending request by typing URL `http://127.0.0.1:8000/` in the web browser. (Or using API tool such as Postman)

Case 1: If the request is not with GET method
```
http status code: 405 (Method Not Allowed)
{
  "status": "false",
  "message": "POST method is not allowed, only GET method is accepted."
}
```
![405 Method Not Allowed](https://github.com/sombra721/rate_limiter/blob/main/RateLimiter/img/status_405.jpg)

Case 2: If the number of requests the user made exceeds the rate limitation
```
http status code: 429 (Too Many Requests)
{
  "status": "false",
  "message": "There are too many requests in a given amount of time (more than 5 requests in past 3000 milliseconds)"
}
```
![429 Too Many Request](https://github.com/sombra721/rate_limiter/blob/main/RateLimiter/img/status_429.jpg)

Case 3: If the number of requests the user made does not exceed the rate limitation
```
http status code: 200 (OK)
{
  "status": "true",
  "message": "Current time: 2023/09/08 23:31:19 UTC"
}
```
![200 OK](https://github.com/sombra721/rate_limiter/blob/main/RateLimiter/img/status_200.jpg)

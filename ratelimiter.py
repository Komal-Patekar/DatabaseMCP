import time
from config import MAX_QUERIES_PER_MINUTE

request_times = []

def check_rate_limit():
    now = time.time()

    # keep only last minute
    while request_times and request_times[0] < now - 60:
        request_times.pop(0)

    if len(request_times) >= MAX_QUERIES_PER_MINUTE:
        raise Exception("Rate limit exceeded")

    request_times.append(now)

mport functools
import time
import requests
from requests.exceptions import RequestException

def cache_result(expiration_time=10):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            if url not in cache or time.time() - cache[url]['timestamp'] > expiration_time:
                cache[url] = {'timestamp': time.time(), 'result': func(*args, **kwargs)}
            elif 'result' not in cache[url]:
                cache[url]['result'] = func(*args, **kwargs)
            print(f"URL '{url}' accessed {cache[url]['count']} times.")
            cache[url]['count'] += 1
            return cache[url]['result']

        return wrapper

    return decorator

@cache_result()
def get_page(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error while fetching URL '{url}': {e}")
        return ""

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http%3A%2F%2Fexample.com"
    print(get_page(url))
    print(get_page(url))
    time.sleep(11)
    print(get_page(url))

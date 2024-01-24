#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """Decorator counting how many times a URL is accessed.

    Args:
        method (function): The original function to be decorated.

    Returns:
        function: The wrapper function.
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function for counting URL accesses and caching."""
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Returns HTML content of a URL.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content.
    """
    res = requests.get(url)
    return res.text

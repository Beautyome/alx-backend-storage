#!/usr/bin/env python3

import requests
import time
from cachetools import TTLCache

# Create a TTLCache with a maximum size of 100 and a TTL (time-to-live) of 10 seconds
url_cache = TTLCache(maxsize=100, ttl=10)

# Function to get the page content (decorated with cache_and_track)
def cache_and_track(func):
    def wrapper(url):
        # Check if the URL is in the cache
        if url in url_cache:
            # Return the cached result
            return url_cache[url]

        # Make the request to the URL and fetch the content
        response = requests.get(url)
        page_content = response.text

        # Update the URL access count
        url_access_count[url] = url_access_count.get(url, 0) + 1

        # Cache the result with a TTL of 10 seconds
        url_cache[url] = page_content

        time.sleep(10)  # Simulate slow response

        return page_content

    return wrapper

# Function to get the page content (decorated with cache_and_track)
@cache_and_track
def get_page(url: str) -> str:
    return url

# Example usage
if __name__ == "__main__":
    url_ = "http://slowwly.robertomurray.co.uk/delay/1000/url/"
    url = f"{url_}http://www.google.com"
    print(get_page(url))
    print(get_page(url))
    print(f"Access count for {url}: {url_access_count[url]}")

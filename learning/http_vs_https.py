# Why does `https` not work when I make a request to PG's articles page, but `http` does?

import requests


class HTTPSVsHTTP:
    def __init__(self):
        self.https_url = "https://www.paulgraham.com/articles.html"
        self.http_url = "http://www.paulgraham.com/articles.html"

        self.https_r = requests.get(self.https_url)  # TODO: Why does this not work? Come back to this again
        self.http_r = requests.get(self.http_url)




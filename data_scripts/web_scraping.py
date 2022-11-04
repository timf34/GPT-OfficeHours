import requests
from urllib import request

from bs4 import BeautifulSoup


class PaulGrahamScraper:
    def __init__(self):
        self.url = "http://www.paulgraham.com/articles.html"
        self.r = requests.get(self.url)
        self.html = request.urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html, "html.parser")


def main():
    scraper = PaulGrahamScraper()




if __name__ == "__main__":
    main()


import bs4

from bs4 import BeautifulSoup
from typing import List, Dict
from urllib import request


class PaulGrahamScraper:
    def __init__(self):
        self.url: str = "http://www.paulgraham.com/articles.html"
        self.html: str = request.urlopen(self.url).read()
        self.soup: bs4.BeautifulSoup = BeautifulSoup(self.html, "html.parser")
        self.articles: List = []

    def get_articles(self) -> None:
        # There are 4 tables; t1 -> the following 3; t2 -> the intro; t3 -> the articles; t4 -> the footer (rss link)
        articles_table = self.soup.find_all("table")[2]

        # Find all articles (they will end with '.html')
        for link in articles_table.find_all("a"):
            if link.get("href").endswith(".html"):
                self.articles.append(link.get("href"))


def main():
    scraper = PaulGrahamScraper()
    scraper.get_articles()


if __name__ == "__main__":
    main()


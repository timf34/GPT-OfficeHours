import bs4

from bs4 import BeautifulSoup
from typing import List, Dict
from urllib import request


class PaulGrahamScraper:
    def __init__(self):
        self.url: str = "http://www.paulgraham.com/articles.html"
        self.base_url: str = "http://www.paulgraham.com/"
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

        # Remove duplicates
        self.articles = list(set(self.articles))

    def get_article_data(self) -> List[Dict]:
        article_data: List[Dict] = []

        for article in self.articles:
            print(article)
            article_html: str = request.urlopen(self.base_url + article).read()
            # print(article_html)
            article_soup: bs4.BeautifulSoup = BeautifulSoup(article_html, "html.parser")
            # print(article_soup.text)

            # Get article title; which is the alt within the first img tag
            article_titles: str = [x.get("alt") for x in article_soup.find_all("img")]
            # Filter out None values
            article_titles = list(filter(None, article_titles))
            # Check if there is a title
            if len(article_titles) > 0:
                article_title: str = article_titles[0]
                print(article_title)

            # We can also get the title from the title tag
            article_title = article_soup.title.string
            print(article_title)
            break

        return article_data


def main():
    scraper = PaulGrahamScraper()
    scraper.get_articles()
    article_data = scraper.get_article_data()


if __name__ == "__main__":
    main()


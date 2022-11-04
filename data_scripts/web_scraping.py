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
            # article_html: str = request.urlopen(self.base_url + article).read()
            article_html: str = request.urlopen("http://paulgraham.com/notnot.html").read()
            article_soup: bs4.BeautifulSoup = BeautifulSoup(article_html, "html.parser")

            # Get article title from title tag
            article_title = article_soup.title.string

            # Get the article content, contained in the 2nd table
            article_content = article_soup.find_all("table")[1]

            # Get the text from the article content
            article_text = article_content.get_text()
            print(article_text)





            break
            # TODO: note that this has probably gotten unneccesarily complicated.
            #  The recursion is to work with the case of a different file structure as we have for notnot.html
            #  However I can now see that this doesn't work for our normal essays!
            #  I am quite certainly over complicating things here, and would be best off just using the .get_text() method
            #  or the .text attribute!!!! It't not that big a deal to also have footers in it.
            #  And remember that we are not looking for a perfect thing right now, we just want to get through all the
            #  steps of this project so I can do as much learning as possible, and not get stuck on any one thing.
            #  Once I have Mach 1 done, I can go back and make it better!
            #  I am going to remove all of this code now, after I make a new branch and commit as a checkpoint.
            #  I will leave this comment here for a little while as a reminder of what I was thinking, and what I need to do!

        return article_data

def main():
    scraper = PaulGrahamScraper()
    scraper.get_articles()
    article_data = scraper.get_article_data()


if __name__ == "__main__":
    main()


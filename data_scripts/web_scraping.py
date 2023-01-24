import bs4
import time

from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from urllib import request

# Note: how should the web scraping work?
# It should create a list of articles/ urls for the articles.
# Then it should go through each article and get the data (essay) from each article.


# Other previous note:
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


class PaulGrahamScraper:
    def __init__(self):
        self.url: str = "http://www.paulgraham.com/articles.html"
        self.base_url: str = "http://www.paulgraham.com/"
        self.html: str = request.urlopen(self.url).read()
        self.soup: bs4.BeautifulSoup = BeautifulSoup(self.html, "html.parser")
        self.articles: List = self.get_articles()

    def get_articles(self) -> List:
        """
        Gets and sets all the article URLs from the main page
        :return:
        """
        articles: List = []

        # There are 4 tables; t1 -> the following 3 (its a parent table); t2 -> the intro; t3 -> the articles;
        # t4 -> the footer (rss link)
        articles_table = self.soup.find_all("table")[2]

        # Find all articles (they will end with '.html')
        for link in articles_table.find_all("a"):
            if link.get("href").endswith(".html"):
                articles.append(link.get("href"))

        # Remove duplicates
        return list(set(articles))

    def get_article_content(self, article_url: str) -> Tuple[str, str]:
        """Given an article URL, returns the title and content of the article (soup style!)"""

        if not article_url.startswith("http"):  # If the article string doesn't start with 'http', then it is a relative link
            article_url = self.base_url + article_url

        article_html: str = request.urlopen(article_url).read()
        article_soup: bs4.BeautifulSoup = BeautifulSoup(article_html, "html.parser")
        article_title = article_soup.title.string  # Get article title from title tag
        article_content = article_soup.find_all("table")[1].text  # Get the article content, contained in the 2nd table

        return article_title, article_content

    def get_article_data(self, articles: List[str]) -> List[Dict]:
        article_data: List[Dict] = []

        for article in articles:
            print(article)

            article_title, article_content = self.get_article_content(article)

            # Clean data

            # Remove newlines greater than 1 (i.e. \n\n -> \n or \n\n\n\n\n -> \n, or \n\n\n -> \n)
            for i in range(2, 10):
                article_content = article_content.replace("\n" * i, "\n")

            # article_text = ""
            # for text in article_content.find_all("font")[0].stripped_strings:
            #     article_text += text + "\n"

            article_data.append({"title": article_title, "content": article_content})
            time.sleep(2)
            print(article_data[0]["content"])

        return article_data

def compare_scraping_methods():
    pass


def main():
    scraper = PaulGrahamScraper()

    # Test cases for get_article_data
    test_cases = ["http://www.paulgraham.com/smart.html", "http://paulgraham.com/notnot.html"]

    print(scraper.get_article_data(test_cases))


if __name__ == "__main__":
    main()


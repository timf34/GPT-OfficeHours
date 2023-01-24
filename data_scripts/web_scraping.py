import bs4
import os
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
    def __init__(self, rewrite_files: bool = False):
        self.url: str = "http://www.paulgraham.com/articles.html"
        self.base_url: str = "http://www.paulgraham.com/"
        self.html: str = request.urlopen(self.url).read()
        self.soup: bs4.BeautifulSoup = BeautifulSoup(self.html, "html.parser")
        self.articles: List = self.get_articles()
        self.articles_dir: str = "../data/pg_essays/"
        self.rewrite_files: bool = rewrite_files

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

    @staticmethod
    def clean_article_content(article_content: str) -> str:
        """Cleans/ preprocesses the raw article content"""
        # TODO: I can improve this going forward. Should be good enough for now.
        # Remove newlines greater than 1 (i.e. \n\n -> \n or \n\n\n\n\n -> \n, or \n\n\n -> \n)
        for i in range(2, 10):
            article_content = article_content.replace("\n" * i, "\n")

        return article_content

    def create_txt_file(self, article_title: str, article_content: str) -> None:
        """Create a .txt file for each article in the self.articles_dir directory. Note that we concatenate the title"""
        # Remove white spaces from article title
        article_title = article_title.replace(" ", "_")

        # Remove invalid characters from article title
        illegal_characters = [":", "?", "/", "\\", "*", "|", "<", ">", '"', "'",
                              "!", "@", "#", "$", "%", "^", "&", "(", ")", "-"]
        for character in illegal_characters:
            article_title = article_title.replace(character, "")

        if (
            os.path.exists(self.articles_dir + article_title + ".txt")
            and not self.rewrite_files
        ):
            print("File already exists, skipping...")
            return
        # Encode the article content as utf-8
        article_content = article_content.encode("utf-8")
        with open(self.articles_dir + article_title + ".txt", "wb") as f:
            f.write(article_content)

    def get_article_data(self, articles: List[str]) -> List[Dict]:
        article_data: List[Dict] = []

        for article in articles:
            print(article)

            article_title, article_content = self.get_article_content(article)

            # Clean data...
            self.clean_article_content(article_content)
            # Create a .txt file for each article
            self.create_txt_file(article_title, article_content)
            article_data.append({"title": article_title, "content": article_content})

        return article_data


def experimenting() -> None:
    scraper = PaulGrahamScraper()
    test_cases = ["http://www.paulgraham.com/smart.html", "http://paulgraham.com/notnot.html", "http://www.paulgraham.com/airbnbs.html"]
    print(scraper.get_article_data(test_cases))


def prepare_all_articles() -> None:
    scraper = PaulGrahamScraper()
    scraper.get_article_data(scraper.articles)


def main():
    prepare_all_articles()


if __name__ == "__main__":
    main()


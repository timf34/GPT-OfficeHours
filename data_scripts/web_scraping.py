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

            # Iterate through text in the first <font> tag, then iterate through the texts the <br> tags within that
            article_text = ""

            # if article_content.find_all("font")[0].contents contains <br> tags, then let that be our iterator list
            # else, let the first <p> tag be our iterator list
            if article_content.find_all("font")[0].find_all("br"):
                x = article_content.find_all("font")[0]
                iterator_list = article_content.find_all("font")[0].contents
            else:
                iterator_list = article_content.find_all("p")
                print(iterator_list)


            article_text = self.extract_text(iterator_list)

            print(article_text)


            break

        return article_data

    def extract_text(self, iterator_list: List) -> str:
        article_text = ""
        for text in iterator_list:
            if isinstance(text, bs4.element.Tag):
                if text.name == "p":
                    return self.extract_text(text)  # Note: this assumes one level of <p> tags
                else:
                    article_text += "" if text.string is None else text.string  # Else is for if it's a hyperlink or such.
            else:
                article_text += text + "\n"
        return article_text

def main():
    scraper = PaulGrahamScraper()
    scraper.get_articles()
    article_data = scraper.get_article_data()


if __name__ == "__main__":
    main()


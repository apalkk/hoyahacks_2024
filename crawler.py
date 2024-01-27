import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        iteration = 0
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            try:
                print(url)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html")
                file = open("Admissions/admissions" +
                            str(iteration) + ".txt", 'w')
                file.write(soup.text)
                logging.info(f'Crawling: {url}')
                iteration += 1
                if iteration == 50:
                    exit()
            except Exception:
                print(f"Couldn't format: {url}")
            finally:
                try:
                    self.crawl(url)
                except Exception:
                    logging.exception(f'Failed to crawl: {url}')
                finally:
                    print(self.urls_to_visit)
                    self.visited_urls.append(url)


if __name__ == '__main__':
    Crawler(urls=['https://admissions.umd.edu/']).run()

"""
Module to import the citations of an specific author from her Google's scholar page
"""
# sys modules
import time

# 3rd party modules
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import sys
class GoogleCitationsSpider(scrapy.Spider):
    """
    Class that creates a spider for the citations page
    """
    name = 'gcspider' # for scrapy

    def __init__(self, url='', user='', **kwargs):
        self.urls = (url.format(user, start) for start in range(0, 5000, 100))
        self.start_urls = [next(self.urls)]
        super().__init__(**kwargs)

    def parse(self, response):
        """
        Method used to parse the page from citations.
        Note that we do a trick to limit the results to 100 and move to the next page
        if there are articles left. Otherwise we stop the process.
        """
        # step 1: check if the page was found
        if response.status == 404:
            raise CloseSpider('Page not found exception')
            return None
        # step 2: if found, then check if there are articles in it
        articles = response.css('td.gsc_a_t')
        if len(articles) == 0:
            raise CloseSpider('No articles found')
            return None
        # step 3: for each article found, grab the title and return it
        for article in articles:
            yield {'title': article.css('a ::text').extract_first()}
        # step 4: wait 5 secs to be nice
        time.sleep(5)

        # step 5: follow the next url in the generator
        yield response.follow(next(self.urls), self.parse)

def main():
    """
    The entry point of the application, if called directly from the command line.
    """
    # step 1: define the user to be crawled
    #user = 'kEHKsr8AAAAJ'
    user = sys.argv[1]
    # step 2: create the crawling process, passing the citations url and the user
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': '{}.json'.format(user)
    })
    process.crawl(
        GoogleCitationsSpider,
        url='https://scholar.google.com/citations?user={}&cstart={}&pagesize=100',
        user=user
    )
    # step 3: start crawling!
    process.start() # the script will block here until the crawling is finished

if __name__ == '__main__':
    main()

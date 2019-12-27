import json

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

from src.utils.constants import Constants


class AzlyricsSpider(Spider):
    name = "azlyrics_spider"

    def __init__(self, config):
        super(AzlyricsSpider, self).__init__()
        self.__url__ = config[Constants.CONFIG_KEY_URL]
        # self.__artists__ = config.get(Constants.CONFIG_KEY_ARTISTS, None)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super(AzlyricsSpider, cls).from_crawler(crawler, crawler.settings)

    def start_requests(self):
        yield Request(self.__url__, callback=self.__artist_urls__)

    def __artist_urls__(self, response):
        '''
        for l in LinkExtractor(allow=Constants.REGEX_GENRES_BOOKLIST_URL).extract_links(response):
            print(l.url)
        '''
        for genre_link in LinkExtractor(allow=Constants.REGEX_GENRES_BOOKLIST_URL).extract_links(response):
            print("REGEX_GENRES_BOOKLIST_URL: {}".format(genre_link.url))
            yield Request(url=genre_link.url, callback=self.__artist_track_urls__)

    def parse(self, response):
        links = []

        for row in response.css(Constants.SELECTOR_GENRE_LINK):
            proxy_info = row.css(Constants.SELECTOR_PROXY_INFO).getall()

            # If HTTPS "yes" then add to proxy list
            links.append("{ip}:{port}".format(ip=proxy_info[0], port=proxy_info[1]))



    def __artist_track_urls__(self, response):
        for link in LinkExtractor(allow=Constants.REGEX_GENRE).extract_links(response):
            print("REGEX_GENRE: {}".format(link.url))

            # yield Request(url=link.url, callback=self.__genre_booklists_pagination_urls, cb_kwargs={
            #     Constants.KEY_GENRE_BASE_URL: link.url,
            #     Constants.KEY_GENRE_TITLE: response.css(Constants.SELECTOR_GENRE_TITLE).get()
            # })

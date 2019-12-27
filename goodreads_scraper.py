# Written by Mutlu Polatcan
# 03.12.2019
import json
import yaml
from sys import argv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from src.spiders.proxy_spider import ProxySpider
from src.spiders.azlyrics_spider import AzlyricsSpider
from src.utils.constants import Constants


class SpotipyLyricsScraper:
    def __init__(self, config_filename):
        self.__config = yaml.safe_load(open(config_filename, "r"))
        self.__runner = CrawlerRunner()

    def __load_crawler_settings(self):
        ProxySpider.custom_settings = self.__config[Constants.CONFIG_KEY_PROXY]
        AzlyricsSpider.custom_settings = self.__config[Constants.CONFIG_KEY_AZLYRICS]

    @defer.inlineCallbacks
    def __run_spiders_sequentially(self):
        yield self.__runner.crawl(ProxySpider)

        AzlyricsSpider.custom_settings.update({
            Constants.KEY_ROTATING_PROXY_LIST: json.load(
                open(self.__config[Constants.CONFIG_KEY_PROXY][Constants.CONFIG_KEY_OUTPUT_FILENAME], "r")
                )})

        yield self.__runner.crawl(AzlyricsSpider)

        reactor.stop()

    def run(self):
        configure_logging()
        self.__load_crawler_settings()
        self.__run_spiders_sequentially()
        reactor.run()


if __name__ == "__main__":
    SpotipyLyricsScraper(argv[1]).run()

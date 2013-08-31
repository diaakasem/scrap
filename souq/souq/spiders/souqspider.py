# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from souq.items import SouqItem
# from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from scrapy.http import Request

# Used together
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.contrib.spiders import CSVFeedSpider
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.loader import XPathItemLoader



class SouqSpider(CrawlSpider): 

    name = 'souq.com'
    allowed_domains = ['souq.com']
    start_urls = ['http://deals.souq.com/ae-en/index.php?ajax=1&start=69&tag_color=red&id_tag=14&pid_tag=101']
    rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse_item(self, response):
        x = HtmlXPathSelector(response)
        print response
        item = SouqItem()
        # item['title'] = response.url
        # item['name'] = x.select("//h1/text()").extract()
        # item['description'] = x.select("//div[@id='description']").extract() torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract() return torrent

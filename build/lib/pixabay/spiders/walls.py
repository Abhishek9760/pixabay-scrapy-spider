# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from pixabay.items import PixabayItem

class WallsSpider(Spider):
    name = 'walls'
    allowed_domains = ['pixabay.com']
    # start_urls = ['http://pixabay.com/']

    def __init__(self, query):
        self.start_urls = [r"https://www.pixabay.com/images/search/" + query]

    def parse(self, response):
        links = [response.urljoin(link) for link in response.xpath('//div[@class="item"]/a/@href').extract()]
        for link in links:
            yield Request(link, callback=self.parse_page)

        next_page_url = response.urljoin(response.xpath('//link[@rel="next"]/@href').extract_first())
        yield Request(next_page_url)

    def parse_page(self, response):
        l = ItemLoader(item=PixabayItem(), response=response)
        image_urls = response.xpath("//a[@rel='license']/@about").extract_first()
        l.add_value('image_urls', image_urls)
        yield {
        'URL': image_urls,
        'image_urls' :[image_urls]
        }
        return l.load_item()

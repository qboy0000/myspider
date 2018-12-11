# -*- coding: utf-8 -*-
import scrapy

from myspider.items import NvdFeedItem

class NvdSpider(scrapy.Spider):
    name = 'nvdfeed'
    allowed_domains = ['nvd.nist.gov','static.nvd.nist.gov']
    start_urls = ['https://nvd.nist.gov/vuln/data-feeds']

    def parse(self, response):

        json_urls = response.xpath('//table[@data-testid="vuln-feed-table"]/tbody/tr[re:test(@data-testid,"vuln-json-feed-row-*gzip*")]/td[1]/a/@href').extract()
        print json_urls
        # item = NvdFeedItem()
        # item['file_urls'] = json_urls
        # yield item
        for j in json_urls:
            item = NvdFeedItem()
            item['file_urls'] = [j]
            yield item

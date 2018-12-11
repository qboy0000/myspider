# -*- coding: utf-8 -*-
import scrapy
from myspider.items import TalosIntelligenceItem

class TalosintelligenceSpider(scrapy.Spider):
    name = 'talosintelligence'
    allowed_domains = ['www.talosintelligence.com']
    start_urls = ['https://www.talosintelligence.com/vulnerability_reports#disclosed/']

    def parse(self, response):
        data_urls = response.xpath('//table[@id="vul-report"]/tbody/tr/@data-url').extract()

        for url in data_urls:
            report_id = url.split('/')[-1]
            print report_id
            item = TalosIntelligenceItem()
            item['report_id'] = report_id
            yield item

            # yield scrapy.Request(url='https://www.talosintelligence.com{}'.format(url),callback=self.parse_item)

    def parse_item(self,response):
        pass
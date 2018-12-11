# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import scrapy
from myspider.items import MacVendorItem
class MacVendorLookUpSpider(scrapy.Spider):
    name = 'macvendorlookup'
    allowed_domains = ["www.macvendorlookup.com"]

    def start_requests(self):
        return [scrapy.FormRequest("https://www.macvendorlookup.com/browse/",
                                   callback=self.parseItem)]

    def parseDetail(self,response):
        xdetail = lambda x: response.xpath(x).extract_first().replace('\r', '').replace('\n', '').replace('\t', '').strip() if response.xpath(x).extract_first() is not None else None

        item = MacVendorItem()
        item['company'] = xdetail('/html/body/div[2]/div[2]/div[1]/div/div/dl/dd[1]/strong/text()')
        item['mac_prefix'] = xdetail('/html/body/div[2]/div[2]/div[1]/div/div/dl/dd[3]/code/text()')[:8]
        item['type'] = xdetail('/html/body/div[2]/div[2]/div[1]/div/div/dl/dd[4]/text()')
        address = xdetail('/html/body/div[2]/div[2]/div[1]/div/div/dl/dd[2]/address').replace('<address>','').replace('</address>','')
        item['address'] = address
        yield item

    def parseItem(self, response):
        print 'text===>'
        # print uincode('中国').encode('utf-8')

        # print response.body
        item_trs = response.xpath('/html/body/div[2]/div[2]/div[1]/div/div/table/tbody/tr')
        if len(item_trs) >0:

            for tr in item_trs:

                detail_url = tr.xpath('td[3]/a/@href').extract_first()
                yield scrapy.Request(url="https://www.macvendorlookup.com{}".format(detail_url), callback=self.parseDetail)
                # print item
                # yield item
            next_url = response.xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div/ul[1]/li[2]/a/@href').extract_first()
            yield scrapy.Request(url="https://www.macvendorlookup.com{}".format(next_url),callback=self.parseItem)
# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import scrapy
from myspider.items import PortInfoItem

class PortInfoSpider(scrapy.Spider):
    name = 'port_info'
    allowed_domains = ["www.grc.com"]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest("https://www.grc.com/port_{}.htm".format(i),
                               # formdata={'qstartdate': '2018-03-01', 'qenddate': '2018-03-01'},
                               callback=self.parseItem) for i in range(0,65536)]


    def parseItem(self, response):

        try:
            print 'text===>'
            # print response.text
            # print uincode('中国').encode('utf-8')
            tmp = response.xpath('//table[2]/tr[1]/td[1]/table[1]/tr[4]/td[2]/font[1]/a')
            xdetail = lambda x: response.xpath(x).extract_first().replace('\r', '').replace('\n', '').replace(
                '\t', '').strip() if response.xpath(x).extract_first() is not None else ''
            item = PortInfoItem()

            item['port'] = int(xdetail('//font[@color="#CC0033"]/b/text()').replace('Port ',''))
            item['name'] = xdetail('//table[2]/tr[1]/td[1]/table[1]/tr[1]/td[2]/font[1]/b/text()')
            item['purpose'] = xdetail('//table[2]/tr[1]/td[1]/table[1]/tr[2]/td[2]/font[1]/b/text()')
            item['description'] = xdetail('//table[2]/tr[1]/td[1]/table[1]/tr[3]/td[2]/font[1]/text()')

            item['related_ports'] = response.xpath('//table[2]/tr[1]/td[1]/table[1]/tr[4]/td[2]/font[1]/a/text()').extract()
            item['additional_information'] = response.xpath('/html/body/center/form/table[3]/tr/td').extract_first()
            yield item
        except Exception as ex:
            print ex

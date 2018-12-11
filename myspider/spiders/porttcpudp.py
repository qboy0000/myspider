# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import scrapy
from myspider.items import PortTcpUdpItem

class PortTcpUdpItemSpider(scrapy.Spider):
    name = 'port_tcp_udp'
    allowed_domains = ["www.speedguide.net"]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest("https://www.speedguide.net/port.php?port={}".format(i),
                               # formdata={'qstartdate': '2018-03-01', 'qenddate': '2018-03-01'},
                               callback=self.parseItem) for i in range(3800,5000)]


    def parseItem(self, response):

        try:

            tmp = response.xpath('//table[2]/tr[1]/td[1]/table[1]/tr[4]/td[2]/font[1]/a')
            xdetail = lambda x: response.xpath(x).extract_first().replace('\r', '').replace('\n', '').replace(
                '\t', '').strip() if response.xpath(x).extract_first() is not None else ''
            tr_detail = lambda x,tr: tr.xpath(x).extract_first().strip() if tr.xpath(x).extract_first() is not None else ''
            item = PortTcpUdpItem()
            item['port'] = int(xdetail('//h1[@class="title"]/text()').split(' ')[1])
            port_detail = []
            tr_items = response.xpath('//table[@class="port"]/tr')
            if len(tr_items) >=2:
                for i in range(1,len(tr_items)):
                    title = tr_items[i].xpath('@title').extract_first()
                    updated,hits = title.split(',')

                    ports = tr_detail('td[1]/text()',tr_items[i])
                    protocol =tr_detail('td[2]/text()',tr_items[i])
                    service = tr_detail('td[3]/text()',tr_items[i])
                    details = tr_detail('td[4]/text()',tr_items[i])
                    source = tr_detail('td[5]/text()',tr_items[i])
                    port_detail.append({
                        'updated':updated.split(":")[1],
                        'hits':hits.split(':')[1],
                        'ports':ports,
                        'protocol':protocol,
                        'service': service,
                        'details': details,
                        'source': source
                    })
            item['detail'] = port_detail
            yield item
        except Exception as ex:
            print ex

# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import scrapy
from myspider.items import CnnvdvulItem
class CNNVDSpider(scrapy.Spider):
    name = 'cnnvd'
    allowed_domains = ["www.cnnvd.org.cn"]
    # start_urls = [
    #     'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201201-358'
    # ]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest("http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno=1&repairLd=",
                                   # formdata={'qstartdate': '2018-03-01', 'qenddate': '2018-03-01'},
                                   callback=self.parse_first_page)]

    def parse_first_page(self,response):

        pagecount = int(response.xpath('//input[@id="pagecount"]/@value').extract_first())
        print "parse_first_page",pagecount
        for i in range(1,pagecount+1):
            print "parse page ",i
            yield scrapy.FormRequest(url="http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno={}&repairLd=".format(i),
                                 # formdata={'qstartdate': '2018-03-01', 'qenddate': '2018-03-01'},
                                 callback=self.parse_list)

        self.parse_list(response=response)

    def parse_list(self,response):
        weblist = response.xpath('//a[@class="a_title2"]/@href').extract()
        for web in weblist:
            print "parse_list==>",web
            yield scrapy.Request(url="http://www.cnnvd.org.cn{}".format(web),callback=self.parseItem)

    def parseItem(self, response):
        print 'text===>'
        # print uincode('中国').encode('utf-8')
        item = CnnvdvulItem()
        # print response.body
        item_sel = response.xpath('//div[contains(@class,"container")]/div[contains(@class,"container")]/div[contains(@class,"fl")]')
        print item_sel
        item_detail_sel = item_sel.xpath('div[contains(@class,"detail_xq")]')
        item['vuln_title'] = item_detail_sel.xpath('h2/text()').extract_first()

        # xdetail = lambda x: item_detail_sel.xpath(x).extract_first().encode('unicode-escape').decode('string_escape').replace('\r','').replace('\n','').replace('\t','').strip()
        xdetail = lambda x: item_detail_sel.xpath(x).extract_first().replace('\r', '').replace('\n', '').replace('\t', '').strip() if item_detail_sel.xpath(x).extract_first() is not None else None

        cnnvd_id = xdetail('ul/li[1]/span/text()')
        item['cnnvd_id']=cnnvd_id[-16:]
        item['vuln_severity']=xdetail('ul/li[2]/a/text()')
        item['cve_id'] =xdetail('ul/li[3]/a/text()')
        item['vuln_type']=xdetail('ul/li[4]/a/text()')
        item['vuln_published'] = xdetail('ul/li[5]/a/text()')
        item['vuln_used_style'] = xdetail('ul/li[6]/a/text()')
        item['vuln_modified'] = xdetail('ul/li[7]/a/text()')
        item['vuln_manufacturer_name']=xdetail('ul/li[8]/a/text()')
        item['vuln_source'] = xdetail('ul/li[9]/span/text()')[5:]

        desc = item_sel.xpath('div[contains(@class,"d_ldjj")][1]').xpath('p/text()').extract()

        item['vuln_describe'] = '\r\n'.join(desc)

        vuln_refs_arr = item_sel.xpath('div[contains(@class,"d_ldjj")][3]').xpath('p')
        if (len(vuln_refs_arr) >= 2):
            refs_arr=[]

            for i in range((len(vuln_refs_arr)+1)/3):
                source = vuln_refs_arr[i*3].xpath('text()').extract_first().replace('\r', '').replace('\n', '').replace('\t', '').strip()[3:]
                link =vuln_refs_arr[i*3+1].xpath('text()').extract_first().replace('\r', '').replace('\n', '').replace('\t', '').strip()[3:]
                # print source.encode('unicode-escape').decode('string_escape'),link
                refs_arr.append({'source':source,'link':link})
            item['vuln_refs'] = refs_arr

        vuln_version_arr = item_sel.xpath('div[contains(@class,"d_ldjj")][4]/div[contains(@class,"vulnerability_list")]/ul/li/div/a/text()').extract()
        # if len(vuln_version_arr) >0:
            # vuln_versions = [ver.replace('\r', '').replace('\n', '').replace('\t', '').strip() for ver in vuln_version_arr ]
        item['vuln_version_number'] = vuln_version_arr

        vuln_solution_arr = item_sel.xpath(
            'div[contains(@class,"d_ldjj")][5]/div[contains(@class,"vulnerability_list")]/ul/li/div/a/@href').extract()

        item['vuln_solution'] = vuln_solution_arr

        print item
        yield item

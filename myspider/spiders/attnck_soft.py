# -*- coding: utf-8 -*-
import scrapy

from myspider.items import SoftTechItem,SoftItem

class AttnCKSoftSpider(scrapy.Spider):
    name = 'attnck_soft'
    allowed_domains = ['attack.mitre.org']
    base_url = "https://attack.mitre.org"
    start_urls = ['https://attack.mitre.org/software/'
                  ]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest(url, callback=self.parse_groups_page) for url in self.start_urls]

    def parse_groups_page(self, response):
        print "parse_tactics_page"
        # print response.body
        tatics_arr = response.xpath('//tbody[@class="bg-white"]/tr')
        tactics_type = response.xpath('//div[@class="container-fluid"]/div[1]/h1/text()').extract_first()
        i = 0
        for tatic in tatics_arr:
            tactic_url = self.base_url + tatic.xpath('td[1]/a/@href').extract_first()
            # id = tatic.xpath('td[1]/a/text()').extract_first()
            soft_name = tatic.xpath('td[1]/a/text()').extract_first()
            # desc = tatic.xpath('td[3]/text()').extract_first()
            # item = TacticsItem()
            # item['url'] = tactic_url
            # item['tactic_id'] = id
            # item['tactic_name'] = name
            # item['description'] = desc
            # item['tactic_type'] = tactics_type.strip('\n').strip()
            # item['order'] = i
            # i +=1
            # yield item

            yield scrapy.Request(tactic_url,self.parse_tatics_detail,meta={"soft_name":soft_name})

    def parse_tatics_detail(self,response):
        soft_url = response.url
        soft_id = soft_url.split('/')[-2]
        soft_name =response.meta["soft_name"]
        # card_body_arr = response.xpath('//div[@class="card-body"]/div')

        tech_arr = response.xpath('//tbody[@class="bg-white"]/tr')
        j = 0
        for tech in tech_arr:

            tech_id = tech.xpath('td[2]/a/text()').extract_first()
            # desc = tech.xpath('td[4]/p').extract_first()
            item = SoftTechItem()
            item['tech_id'] = tech_id
            item['soft_id'] = soft_id
            item['soft_tech'] = soft_id + "_"+tech_id

            j += 1

            yield item

        card_body_arr = response.xpath('//div[@class="card-body"]/div')
        soft_type = card_body_arr[2].xpath('text()').extract_first().lstrip(': ')

        soft_platforms =card_body_arr[4].xpath('text()').extract_first().lstrip(': ')
        soft_version = card_body_arr[5].xpath('text()').extract_first().strip(': ')
        desc = response.xpath('//div[@class="col-md-8 description-body"]/p').extract_first()
        item = SoftItem()
        item['soft_id'] = soft_id
        item['soft_name'] = soft_name
        item['soft_type'] =soft_type
        item['soft_platforms'] = soft_platforms
        item['soft_version'] = soft_version
        item['desc'] = desc

        yield item

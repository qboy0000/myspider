# -*- coding: utf-8 -*-
import scrapy

from myspider.items import TacticsItem,TechniquesItem,TacticTechniquesItem

class AttnCKSpider(scrapy.Spider):
    name = 'attnck'
    allowed_domains = ['attack.mitre.org']
    base_url = "https://attack.mitre.org"
    start_urls = ['https://attack.mitre.org/tactics/enterprise/',
                  'https://attack.mitre.org/tactics/mobile/',
                  'https://attack.mitre.org/tactics/pre/',
                  ]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest(url,callback=self.parse_tactics_page) for url in self.start_urls]

    def parse_tactics_page(self,response):
        print "parse_tactics_page"
        # print response.body
        tatics_arr = response.xpath('//tbody[@class="bg-white"]/tr')
        tactics_type = response.xpath('//div[@class="container-fluid"]/div[1]/h1/text()').extract_first()
        i = 0
        for tatic in tatics_arr:
            tactic_url = self.base_url + tatic.xpath('td[1]/a/@href').extract_first()
            id = tatic.xpath('td[1]/a/text()').extract_first()
            name = tatic.xpath('td[2]/a/text()').extract_first()
            desc = tatic.xpath('td[3]/text()').extract_first()
            item = TacticsItem()
            item['url'] = tactic_url
            item['tactic_id'] = id
            item['tactic_name'] = name
            item['description'] = desc
            item['tactic_type'] = tactics_type.strip('\n').strip()
            item['order'] = i
            i +=1
            yield item

            yield scrapy.Request(tactic_url,self.parse_tatics_detail)

    def parse_tatics_detail(self,response):
        tactic_url = response.url
        tactic_id = tactic_url.split('/')[-2]
        tech_arr = response.xpath('//tbody[@class="bg-white"]/tr')
        j = 0
        for tech in tech_arr:
            tech_url = self.base_url + tech.xpath('td[1]/a/@href').extract_first()
            id = tech.xpath('td[1]/a/text()').extract_first()
            name = tech.xpath('td[2]/a/text()').extract_first()
            desc = tech.xpath('td[3]/p').extract_first()

            item = TechniquesItem()
            item['tech_id'] = id
            item['tech_name'] = name
            item['description'] = desc
            item['url'] = tech_url

            ttItem = TacticTechniquesItem()
            ttItem['tactic_tech_id'] = "{}_{}".format(tactic_id,id)
            ttItem['tactic_id'] = tactic_id
            ttItem['tech_id'] = id
            ttItem['tech_name'] = name
            ttItem['description'] = desc
            ttItem['url'] = tech_url
            ttItem['order'] = j

            j += 1

            yield ttItem

            yield scrapy.Request(tech_url,callback = self.parse_tech_detail,meta=item)

    def parse_tech_detail(self,response):
        meta_item =response.meta
        item = TechniquesItem()
        item['tech_id'] = meta_item['tech_id']
        item['tech_name'] = meta_item['tech_name']
        item['description'] = meta_item['description']
        item['url'] = meta_item['url']
        card_body_arr = response.xpath('//div[@class="card-body"]/div')
        tactic = card_body_arr[2].xpath('text()').extract_first().lstrip(': ')
        platform = card_body_arr[3].xpath('text()').extract_first()
        permissions =card_body_arr[5].xpath('text()').extract_first()
        datasource = card_body_arr[7].xpath('text()').extract_first()
        version = card_body_arr[15].xpath('text()').extract_first().strip(': ')

        item['tactic'] = tactic.strip() if tactic else None
        item['platform'] = platform.strip() if platform else None
        item['permissions_required'] = permissions.strip() if permissions else None
        item['data_sources'] = datasource.strip() if datasource else None
        item['version'] = version.strip() if version else None
        yield item
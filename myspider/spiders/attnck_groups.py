# -*- coding: utf-8 -*-
import scrapy

from myspider.items import GroupTechItem,GroupSoftItem

class AttnCKGroupSpider(scrapy.Spider):
    name = 'attnck_group'
    allowed_domains = ['attack.mitre.org']
    base_url = "https://attack.mitre.org"
    start_urls = ['https://attack.mitre.org/groups/'
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
            gpname = tatic.xpath('td[1]/a/text()').extract_first()
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

            yield scrapy.Request(tactic_url,self.parse_tatics_detail,meta={"groupname":gpname})

    def parse_tatics_detail(self,response):
        group_url = response.url
        group_id = group_url.split('/')[-2]
        gp_name =response.meta["groupname"]
        # card_body_arr = response.xpath('//div[@class="card-body"]/div')

        tech_arr = response.xpath('//table[preceding::h2[@id="techniques"]][1]/tbody[@class="bg-white"]/tr')
        j = 0
        for tech in tech_arr:

            tech_id = tech.xpath('td[2]/a/text()').extract_first()
            # desc = tech.xpath('td[4]/p').extract_first()
            item = GroupTechItem()
            item['tech_id'] = tech_id
            item['group_id'] = group_id
            item['group_tech'] = group_id + "_"+tech_id
            item['group_name'] = gp_name

            j += 1

            yield item

        # tech_arr = response.xpath('//[@id="software"]/following::table[1]/tbody[@class="bg-white"]/tr')
        tech_arr = response.xpath('//table[preceding::h2[@id="software"]][1]/tbody[@class="bg-white"]/tr')
        j = 0
        for tech in tech_arr:
            id = tech.xpath('td[1]/a/text()').extract_first()
            # desc = tech.xpath('td[4]/p').extract_first()
            item = GroupSoftItem()
            item['soft_id'] = id
            item['group_id'] = group_id
            item['group_soft'] = group_id + "_"+id
            item['group_name'] = gp_name

            j += 1

            yield item

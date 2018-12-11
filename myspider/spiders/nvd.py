# -*- coding: utf-8 -*-
import scrapy

from myspider.items import NvdvulItem

class NvdSpider(scrapy.Spider):
    name = 'nvd'
    allowed_domains = ['nvd.nist.gov']
    start_urls = ['https://nvd.nist.gov/vuln/detail/CVE-2016-10096',
                  'https://nvd.nist.gov/vuln/detail/CVE-2017-12627',
                  'https://nvd.nist.gov/vuln/detail/CVE-2017-1000245'
                  ]

    def start_requests(self):
        # yield scrapy.Request(url="http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201609-627", callback=self.parseItem)
        return [scrapy.FormRequest("https://nvd.nist.gov/vuln/full-listing",
                                   callback=self.parse_full_page)]

    def parse_full_page(self,response):
        print "parse_full_page"
        # print response.body
        month_link_arr = response.xpath('//div[@id="page-content"]/div/ul/li/a/@href').extract()
        for m_link in month_link_arr:
            print "parse_full_page:",m_link
            yield scrapy.Request("http://{}{}".format("nvd.nist.gov",m_link),self.parse_cve_list_page)

    def parse_cve_list_page(self,response):
        print "parse_cve_list_page"
        cve_list_arr = response.xpath('//div[@id="page-content"]/div[@class="row"]/span/a/@href').extract()
        for cve_link in cve_list_arr:
            print "parse_cve_list_page",cve_link
            yield scrapy.Request("http://{}{}".format("nvd.nist.gov", cve_link))

    def parse(self, response):
        cve_item = {"cve_id": "page-header-vuln-id",
         "vuln_description": "vuln-description",
         "vuln_description_source": "vuln-description-source",
         "vuln_description_last_modified": "vuln-description-last-modified",
         "vuln_published_on": "vuln-published-on",
         "vuln_last_modified_on": "vuln-last-modified-on",
         "vuln_source": "vuln-source",
         "vuln_cvssv3_base_score": "vuln-cvssv3-base-score-link",
         "vuln_cvssv3_base_score_severity": "vuln-cvssv3-base-score-severity",
         "vuln_cvssv3_vector": "vuln-cvssv3-vector-link",
         "vuln_cvssv3_impact_score": "vuln-cvssv3-impact-score",
         "vuln_cvssv3_exploitability_score": "vuln-cvssv3-exploitability-score",
         "vuln_cvssv3_av": "vuln-cvssv3-av",
         "vuln_cvssv3_ac": "vuln-cvssv3-ac",
         "vuln_cvssv3_pr": "vuln-cvssv3-pr",
         "vuln_cvssv3_ui": "vuln-cvssv3-ui",
         "vuln_cvssv3_s": "vuln-cvssv3-s",
         "vuln_cvssv3_c": "vuln-cvssv3-c",
         "vuln_cvssv3_i": "vuln-cvssv3-i",
         "vuln_cvssv3_a": "vuln-cvssv3-a",
         "vuln_cvssv2_base_score": "vuln-cvssv2-base-score-link",
         "vuln_cvssv2_base_score_severity": "vuln-cvssv2-base-score-severity",
         "vuln_cvssv2_vector": "vuln-cvssv2-vector-link",
         "vuln_cvssv2_impact_subscore": "vuln-cvssv2-impact-subscore",
         "vuln_cvssv2_exploitability_score": "vuln-cvssv2-exploitability-score",
         "vuln_cvssv2_av": "vuln-cvssv2-av",
         "vuln_cvssv2_ac": "vuln-cvssv2-ac",
         "vuln_cvssv2_au": "vuln-cvssv2-au",
         "vuln_cvssv2_i": "vuln-cvssv2-i"}

        trip_value = lambda x:x.replace('\r','').replace('\n','').strip() if x is not None else ""

        item = NvdvulItem()
        for k in cve_item.keys():
            v = response.xpath('//*[@data-testid="{}"]/text()'.format(cve_item[k])).extract_first()
            if v is not None:
                item[k] = trip_value(v)

        index = 0
        hyperlinks=[]
        while(True):
            restype = response.xpath('//*[@data-testid="vuln-hyperlinks-restype-{}"]/text()'.format(index)).extract_first()
            if restype is None:
                break
            else:
                link = response.xpath('//*[@data-testid="vuln-hyperlinks-link-{}"]/a/@href'.format(index)).extract_first()
                type = response.xpath(
                    '//*[@data-testid="vuln-hyperlinks-type-{}"]/text()'.format(index)).extract_first()
                source = response.xpath(
                    '//*[@data-testid="vuln-hyperlinks-source-{}"]/text()'.format(index)).extract_first()
                vulnname = response.xpath(
                    '//*[@data-testid="vuln-hyperlinks-vulnname-{}"]/text()'.format(index)).extract_first()

                hyperlinks.append({
                    'restype':trip_value(restype),
                    'link':trip_value(link),
                    'type':trip_value(type),
                    'source':trip_value(source),
                    'vulnname':trip_value(vulnname)
                })
                index +=1

        item['vuln_hyperlinks'] = hyperlinks

        index = 0
        software_cpe_arr = []
        while(True):
            software_cpe = response.xpath(
                '//*[@data-testid="vuln-software-cpe-1-0-{}"]/a/text()'.format(index)).extract_first()
            if software_cpe is None:
                break
            else:
                software_cpe_arr.append(trip_value(software_cpe))
                index+=1
        item['vuln_software_cpe'] = software_cpe_arr

        print item

        yield item

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItemBase(object):
    collection_name = ""
    key_id = ""


class CnnvdvulItem(scrapy.Item,ItemBase):
    '''
    vuln_title:漏洞标题
    cve_id:漏洞CVE编号
    cnnvd_id:漏洞CNNVD编号
    bugtraq_id:漏洞Bugtraq编号
    vuln_published:漏洞发布时间
    vuln_modified:漏洞更新时间
    vuln_source:漏洞发布单位
    vuln_severity:危害等级
    vuln_type:漏洞类别
    vuln_manufacturer_name:影响厂商/组织名称
    vuln_product_name:影响产品/项目名称
    vuln_version_number:影响版本号
    vuln_describe:漏洞描述
    vuln_solution:补丁信息链接
    vuln_refs:参考地址
    vuln_used_style:威胁类型
    '''
    collection_name = "cnnvd_base"
    key_id = "cnnvd_id"

    # define the fields for your item here like:
    vuln_title = scrapy.Field()
    cve_id = scrapy.Field()
    cnnvd_id = scrapy.Field()
    bugtraq_id = scrapy.Field()
    vuln_published = scrapy.Field()
    vuln_modified = scrapy.Field()
    vuln_source = scrapy.Field()
    vuln_severity = scrapy.Field()
    vuln_type = scrapy.Field()
    vuln_manufacturer_name = scrapy.Field()
    vuln_product_name = scrapy.Field()
    vuln_version_number = scrapy.Field()
    vuln_describe = scrapy.Field()
    vuln_solution = scrapy.Field()
    vuln_refs = scrapy.Field()
    vuln_used_style = scrapy.Field()

    # pass


class NvdvulItem(scrapy.Item,ItemBase):
    collection_name = "nvd_base"
    key_id = "cve_id"

    cve_id = scrapy.Field()
    vuln_description = scrapy.Field()
    vuln_description_source = scrapy.Field()
    vuln_description_last_modified = scrapy.Field()
    vuln_published_on = scrapy.Field()
    vuln_last_modified_on = scrapy.Field()
    vuln_source = scrapy.Field()
    vuln_cvssv3_base_score = scrapy.Field()
    vuln_cvssv3_base_score_severity = scrapy.Field()
    vuln_cvssv3_vector = scrapy.Field()
    vuln_cvssv3_impact_score = scrapy.Field()
    vuln_cvssv3_exploitability_score = scrapy.Field()
    vuln_cvssv3_av = scrapy.Field()
    vuln_cvssv3_ac = scrapy.Field()
    vuln_cvssv3_pr = scrapy.Field()
    vuln_cvssv3_ui = scrapy.Field()
    vuln_cvssv3_s = scrapy.Field()
    vuln_cvssv3_c = scrapy.Field()
    vuln_cvssv3_i = scrapy.Field()
    vuln_cvssv3_a = scrapy.Field()
    vuln_cvssv2_base_score = scrapy.Field()
    vuln_cvssv2_base_score_severity = scrapy.Field()
    vuln_cvssv2_vector = scrapy.Field()
    vuln_cvssv2_impact_subscore = scrapy.Field()
    vuln_cvssv2_exploitability_score = scrapy.Field()
    vuln_cvssv2_av = scrapy.Field()
    vuln_cvssv2_ac = scrapy.Field()
    vuln_cvssv2_au = scrapy.Field()
    vuln_cvssv2_i = scrapy.Field()
    vuln_hyperlinks = scrapy.Field()
    vuln_software_cpe = scrapy.Field()


class ExploitDBItem(scrapy.Item,ItemBase):


    collection_name = "exploitdb_base"
    key_id = "id"

    application_md5 = scrapy.Field()
    application_path = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    code = scrapy.Field()
    date_published = scrapy.Field()
    description = scrapy.Field()
    download = scrapy.Field()
    id = scrapy.Field()
    platform = scrapy.Field()
    platform_id = scrapy.Field()
    port = scrapy.Field()
    screenshot_path = scrapy.Field()
    screenshot_thumb_path = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
    type_id = scrapy.Field()
    verified = scrapy.Field()

    # edb_id = scrapy.Field()
    # author = scrapy.Field()
    # published = scrapy.Field()
    # cve_id = scrapy.Field()
    # vuln_type = scrapy.Field()
    # platform = scrapy.Field()
    # aliases = scrapy.Field()
    # advisory = scrapy.Field()
    # tags = scrapy.Field()
    # verified = scrapy.Field()
    # vuln_app = scrapy.Field()
    # exploit_code = scrapy.Field()
    # related_exploits = scrapy.Field()


class ExploitFileItem(scrapy.Item):
    '''
    NVD Json Feed Item
    '''
    file_prefix = "edb_"
    file_id = scrapy.Field()
    file_urls=scrapy.Field()
    files = scrapy.Field()


class TalosIntelligenceItem(scrapy.Item,ItemBase):
    collection_name = "talosintelligence_base"
    key_id = 'report_id'

    report_id = scrapy.Field()
    title = scrapy.Field()
    title_bd = scrapy.Field()
    cve_id = scrapy.Field()


class NvdFeedItem(scrapy.Item):
    '''
    NVD Json Feed Item
    '''
    file_urls=scrapy.Field()
    files = scrapy.Field()

class MacVendorItem(scrapy.Item,ItemBase):
    '''
    Mac Vendor Item
    '''
    collection_name = "mac_vendor"
    key_id = 'mac_prefix'

    company = scrapy.Field()
    mac_prefix = scrapy.Field()
    type = scrapy.Field()
    address = scrapy.Field()

class PortInfoItem(scrapy.Item,ItemBase):
    '''
    Mac Vendor Item
    '''
    collection_name = "port_info"
    key_id = 'port'

    port = scrapy.Field()
    name = scrapy.Field()
    purpose = scrapy.Field()
    description = scrapy.Field()
    related_ports = scrapy.Field()
    url = scrapy.Field()
    additional_information = scrapy.Field()

class PortTcpUdpItem(scrapy.Item, ItemBase):
    '''
    Mac Vendor Item
    '''
    collection_name = "port_tcp_udp"
    key_id = 'port'

    port = scrapy.Field()
    detail = scrapy.Field()
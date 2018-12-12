# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.pipelines.files import FilesPipeline
import gzip
from items import ItemBase
import json

class CnnvdvulPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        print 'process_item',item
        postItem = dict(item)  # 把item转化成字典形式

        if isinstance(item,ItemBase):
            assert item.collection_name is not  None and len(item.collection_name) > 0 , 'collection_name is null'
            assert item.key_id is not None and len(item.key_id) > 0, 'key_id is null'

            col = self.db[item.collection_name]
            key_id = item.key_id

            print item.collection_name,item.key_id,{key_id:item[key_id]}

            if col.find_one({key_id:item[key_id]}) is None:
                col.insert(postItem)
            else:
                col.update({key_id:item[key_id]},postItem)


        return item  # 会在控制台输出原item数据，可以选择不写

class NVDJSONFeedPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        print "NVDJSONFeedPipeline"
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

        super(NVDJSONFeedPipeline, self).__init__(store_uri=store_uri, download_func=download_func, settings=settings)

    # def file_path(self, request, response=None, info=None):
    #     print request.url
    #     return request.url

    def item_completed(self, results, item, info):

        print "item_completed==>",results,item,info
        col = self.db['cvebase']
        for (r,dict) in results:
            if r:
                with gzip.open(self.store._get_filesystem_path(dict['path']),'rb') as gzipfile:
                    file_content = gzipfile.read()
                    j = json.loads(file_content)
                    for cveitem in j['CVE_Items']:
                        cve_id = cveitem['cve']['CVE_data_meta']['ID']
                        cveitem['cve_id'] = cve_id
                        if col.find_one({'cve_id': cve_id}) is None:
                            col.insert(cveitem)
                        else:
                            col.update({'cve_id': cve_id}, cveitem)
                    gzipfile.close()
        return item

class MyFileDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        print "MyFileDownloadPipeline===>",info,request.url
        file_name = request.url.split('?')[0].split('/')[-1]
        path =  "{}/{}".format(info.spider.name,file_name)
        return path
        # return  super(MyFileDownloadPipeline,self).file_path(request,response=response,info=info)

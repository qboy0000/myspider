# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import httplib
import md5
import urllib
import random
import json
from scrapy.conf import settings
import pymongo
from pymongo.errors import AutoReconnect
from retrying import retry

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关


logfile = "translate.log"
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

appid = ''  # 你的appid
secretKey = ''  # 你的密钥

fromLang = 'en'
toLang = 'zh'
httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')

def translate_baidu(q):
    # global appid,secretKey,fromLang,toLang,httpClient
    # print "translate_baidu==>",q
    logger.debug("translate_baidu==>",q)
    myurl = '/api/trans/vip/translate'
    salt = random.randint(0, 10000)

    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:

        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        json_obj = json.loads(response.read())
        return json_obj['trans_result'][0]['dst']
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def retry_if_auto_reconnect_error(exception):
    '''
    Return True if we should retry (in this case when it's an AutoReconnect), False otherwise
    :param exception:
    :return:
    '''
    return isinstance(exception, AutoReconnect)

class PortInfo():
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.port_table = self.client[settings['MONGO_DB']]['port_info']  # 获得数据库的句柄
    def get_all_port_info(self,skip=0,limit=100):
        queryset = self.port_table.find()
        return queryset.skip(skip).limit(limit)
    def count_port_info(self):
        return self.port_table.count()

    @retry(retry_on_exception=retry_if_auto_reconnect_error, stop_max_attempt_number=2, wait_fixed=2000)
    def update(self,query,update_set):
        self.port_table.update(query,update_set)


if __name__ == "__main__":
    portInfo = PortInfo()

    index = 0
    limit = 200
    count = portInfo.count_port_info()
    while(index * limit < count):
        port_info_list = portInfo.get_all_port_info(index*limit,limit)
        for pi in port_info_list:
            if 'description_bd' not in pi.keys():
                try:
                    logger.info('translage port {}==>'.format(pi['port']))
                    purpose = pi['purpose']
                    purpose_bd = None
                    description_bd = None
                    if purpose is not None and len(purpose) >0:
                        purpose_bd = translate_baidu(purpose)
                    description = pi['description']
                    if description is not None and len(description)>0:
                        description_bd = translate_baidu(description)
                    portInfo.update(pi,{'$set':{'purpose_bd':purpose_bd,'description_bd':description_bd}})
                except Exception as ex:
                    print "[error] ===>",pi['port']
                    logger.error(pi['port'])
                    logger.error(ex)
            else:
                logger.info("{} has translate".format(pi['port']))
        index = index+1
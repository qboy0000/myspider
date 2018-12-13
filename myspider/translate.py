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

appid = '20181213000247791'  # 你的appid
secretKey = 'ph9o2qkU_S_XyDAj1Cl8'  # 你的密钥

fromLang = 'en'
toLang = 'zh'
httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')

def translate(q):
    # global appid,secretKey,fromLang,toLang,httpClient

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

if __name__ == "__main__":
    client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
    # 数据库登录需要帐号密码的话
    # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
    db = client[settings['MONGO_DB']]  # 获得数据库的句柄
    port_info_list = db['port_info'].find()
    for pi in port_info_list:
        purpose = pi['purpose']
        if purpose is not None and len(purpose) >0

    # obj = translate('apple')
    # print obj['trans_result'][0]['dst']
    # obj = translate(
    #     'This is the primary port used by the world wide web (www) system. Web servers open this port then listen for incoming connections from web browsers. Similarly, when a web browser is given a remote address (like grc.com or amazon.com), it assumes that a remote web server will be listening for connections on port 80 at that location.')
    # print obj
    # print obj['trans_result'][0]['dst']
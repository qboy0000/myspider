# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.py

import httplib
import md5
import urllib
import random
import json

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关


logfile = "translate.log"
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

def translate_baidu(q):
    appid = ''  # 你的appid
    secretKey = ''  # 你的密钥

    fromLang = 'en'
    toLang = 'zh'
    httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')

    # global appid,secretKey,fromLang,toLang,httpClient
    # print "translate_baidu==>",q
    logger.debug("translate_baidu==>{}".format(q))
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

def translate_tencent(q):
    url = '''https://tmt.tencentcloudapi.com/?Action=TextTranslate&ProjectId=0&Source=en&SourceText={text}&Target=zh&Version=2018-03-21&Region=ap-beijing'''.format(text=q)
    import requests
    resp = requests.get(url=url)
    print(resp.content)

if __name__ == "__main__":
    translate_tencent("hello")


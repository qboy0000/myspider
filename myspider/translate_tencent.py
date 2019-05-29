# -*- coding: utf-8 -*-
# @author:''
# @filename:$Title.

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

SecretId = "AKIDLuRsr9DF4m3hHEkN2d6I7JV5qvTGL6Sn"
SecretKey = "eYNU6aVKnDTYTHzWwDJH6rTt8XlneJpE"
ProjectId = 1258292245

def translate_tencent(stxt):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

        req = models.TextTranslateRequest()
        # params = '{u"SourceText":"'+str(stxt)+'","Source":"en","Target":"zh","ProjectId":}'
        params = {
            u'SourceText':stxt,
            u'Source':'en',
            u'Target':'zh',
            u'ProjectId':ProjectId
        }
        # req.from_json_string(params)
        req._deserialize(params=params)
        resp = client.TextTranslate(req)
        print(resp.to_json_string())
        return resp.TargetText
    except TencentCloudSDKException as err:
        print(err)

if __name__ == "__main__":
    print translate_tencent("Hello")
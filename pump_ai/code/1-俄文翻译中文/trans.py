import pandas as pd
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import xlrd
import math
#判断语种
def lang(text):
    try: 
        cred = credential.Credential("AKIDQfeMr64lBxTigMmvnNhkW0EBrGOFp78t", "VkhOpzsUptfAOL0OWMvDDxQbWAXdSiiR") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

        req = models.LanguageDetectRequest()
        
        #text = "Дата последнего ремонта"
        params = {
            "Text": text,
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        resp = client.LanguageDetect(req) 
        lang = json.loads(resp.to_json_string())

        #print(resp.to_json_string()) 
        #print(lang["Lang"])
        return lang["Lang"]
    except TencentCloudSDKException as err: 
        print(err)

#翻译
def translate(text):
    try: 
        cred = credential.Credential("AKIDQfeMr64lBxTigMmvnNhkW0EBrGOFp78t", "VkhOpzsUptfAOL0OWMvDDxQbWAXdSiiR") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

        req = models.TextTranslateRequest()
        #lang = lang(text)
        params = {
            "SourceText": text,
            "Source": "ru",
            "Target": "zh",
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextTranslate(req) 
        trantext = json.loads(resp.to_json_string())
        #print(trantext["TargetText"]) 
        return trantext["TargetText"]

    except TencentCloudSDKException as err: 
        print(err) 

#text = "Дата последнего ремонта"

#读取表格
df = pd.read_excel('./testrp.xls')
print(df.head())
n = df.shape[1]
m = df.shape[0]
list = df.values.tolist()


for i in range(n):
    for j in range(m):
        text = list[j][i]
        #判断是不是空值
        if str(text) !='nan':
            langs = lang(text)
            if(langs == "ru"):
                target = translate(text)
                list[j][i] = target
                print(target)

newdf = pd.DataFrame(list)
newdf.to_excel('./outputtest.xls')



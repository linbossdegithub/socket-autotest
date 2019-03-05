#coding=utf-8
import json
import time
import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning

from utils.common.common import getConf, getAllKey
from utils.timeSyn.getTerminalTime import getTimeModel

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def assertControlLog(self,response,description,noApply=[],**kwargs):
    flag = True
    for playername in json.loads(getConf("data", "lite_player")).keys():
        flag1 = False
        for execution in response["data"]["executionList"]:
            if playername == execution["playerName"]:
                flag1 = True
                for key in kwargs.keys():
                    if str(execution[key])!=str(kwargs[key]):
                        flag = False
                        print playername.encode("utf-8") + "日志中的"+key.encode("utf-8")+"值为"+str(execution[key])+" 期望值为"+str(kwargs[key])
                break
        if not flag1:
            if noApply:
                flag88 = False
                for key in getAllKey("searchRes"):
                    if key[-8:]==playername[-8:]:
                        if json.loads(getConf("searchRes",key))["productName"] in noApply :
                            flag88 = True
                if not flag88:
                    flag = False
                    print playername.encode("utf-8") + "没有生成" + description + "日志"

            else:
                flag = False
                print playername.encode("utf-8") + "没有生成"+description+"日志"
    self.assertTrue(flag,description+"日志未全部正确上报")

def getNowTime(addHours = 0):
    time = str((datetime.datetime.now() + datetime.timedelta(hours=addHours)).strftime('%Y-%m-%d %H:%M:%S'))
    return time

def assertTimeModel(self,model=0):
    '''
    :param self: 
    :param model: 3:手动对时    1:NTP对时     2:lora对时
    :return: bool
    '''
    time.sleep(3)
    result = getTimeModel(self)
    flag = True
    for name in json.loads(getConf("data", "lite_player")).keys():
        if result[name.split("-")[1]] != model:
            print name.encode("utf-8") + "对时模式为:" + str(result[name.split("-")[1]])+"    期望值为："+str(model)
            flag = False
    self.assertTrue(flag)
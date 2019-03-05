#coding=utf8
'''
Created on 2018.11.29
@author: chenyongfa
'''
import time

from constant.constant import Constant
from utils.common.common import sendGetCommand

def getTimeConfig(self):
    result = sendGetCommand(self,Constant.WHAT_NET_TIMING,0,Constant.ACTION_GET,0,describe="getTimeConfig")
    return result

def getTimeModel(self):
    '''
    获取终端设置的时间模式
    :param self: 
    :return: 字典，key为sn的后8位（为了匹配'Taurus-40005647'格式）,value为 3(手动)   1(NTP对时)   2(lorad对时)  
    '''
    timeModel = {}
    result = getTimeConfig(self)
    for key in result.keys():
        if result[key]["enable"]:
            if result[key]["ntp"]["enable"]:
                timeModel[key[-8:]] = 1
            if result[key]["lora"]["enable"]:
                timeModel[key[-8:]] = 2
        else:
            timeModel[key[-8:]] = 3
    return timeModel





def getTerminalTime(self):
    '''
    获取终端的时间
    :param    self      必须
    :return   result   字典  返回的data值   {
                                                "utcTimeMillis":1234455433,
                                                "timeZone":"Asia/Shanghai",
                                                "gmt":"GMT+08:00",
                                                "isTimeOffsetEnable":true,
                                                "beginTime":"5-23",
                                                "endTime":"12-23",
                                                "timeOffsetValue":+6000
                                            }
    :example  flag = setTerminalTime(self)
    '''
    localTime = int(round(time.time() * 1000))
    result = sendGetCommand(self,Constant.WHAT_TIME_ZONE,Constant.TYPE_TIME_INFO, Constant.ACTION_GET,0,describe="getTerminalTime")
    return result,localTime

def assertTerminalTimeSyn(self):

    for i in range(5):
        result, localTime = getTerminalTime(self)
        print "当前时间："+str(localTime)
        flag = True
        for i in self.sns:
            if result[i] in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
                flag = False
                print i+":"+result[i]
            else:
                if abs(result[i]["utcTimeMillis"]-localTime)>10000:
                    print str(i)+":"+str(result[i]["utcTimeMillis"])
                    flag = False
        if flag:
            break
        time.sleep(2)
    self.assertTrue(flag, "对时不准确")
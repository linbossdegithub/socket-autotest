#coding=utf8
'''
Created on 2018.11.29
@author: chenyongfa
'''
import json
import threading

import time

from constant.constant import Constant
from utils.common.common import jointArgument, getPacket, sendSetCommand


def getBuffer(flag,ntp,lora):
    buffer = jointArgument(0, 0, Constant.ACTION_SET)
    data = {}
    data["type"] = "NET_TIMING"
    data["source"] = {"type":1,"platform":1}
    data["enable"] = True
    if "cn" in flag.lower():
        data["ntp"] = {"enable":ntp,"server":"ntp1.aliyun.com"}
    else:
        data["ntp"] = {"enable": True, "server": "http://us.ntp.org.cn"}
    data["lora"] = {"address": 1,"channel": 23,"enable":lora,"mode":"MASTER","groupId":"novad101"}
    data["gps"] = {"enable":False}
    data["compatibility"] = {"supportLoraInfo":True}
    buffer = getPacket(param1=Constant.WHAT_NET_TIMING, param2=buffer,data=json.dumps(data))
    return buffer

def setNTPModel(self,node="cn"):
    '''
    设置为NTP对时模式
    :param    self    必须
    :param    node    对时服务器 "cn" 或者 "us"
    :return   flag   bool型
    :example  flag = careRegister(self,"10.20.8.161","chenyongfa")
    '''
    ntp = True
    lora = False
    data = {}
    data["type"] = "NET_TIMING"
    data["source"] = {"type": 1, "platform": 1}
    data["enable"] = True
    if "cn" in node.lower():
        data["ntp"] = {"enable": ntp, "server": "ntp1.aliyun.com"}
    else:
        data["ntp"] = {"enable": True, "server": "http://us.ntp.org.cn"}
    data["lora"] = {"address": 1, "channel": 23, "enable": lora, "mode": "MASTER", "groupId": "novad101"}
    data["gps"] = {"enable": False}
    data["compatibility"] = {"supportLoraInfo": True}

    flag = sendSetCommand(self,Constant.WHAT_NET_TIMING,0, Constant.ACTION_SET,0,data=data,timeout=3,describe="setNTPModel")
    return flag

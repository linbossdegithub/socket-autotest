#coding=utf8
'''
Created on 2018.11.29
@author: chenyongfa
'''
from constant.constant import Constant
from utils.common.common import sendSetCommand
from utils.timeSyn.setNTPModel import setNTPModel


def setManualModel(self):
    '''
    :param self: 必须
    :return:  flag  bool
    example:  flag = setManualModel(self)
    
    '''
    ntp = False
    lora = False
    data = {}
    data["type"] = "NET_TIMING"
    data["source"] = {"type": 1, "platform": 1}
    data["enable"] = True
    data["ntp"] = {"enable": ntp, "server": "ntp1.aliyun.com"}
    data["lora"] = {"address": 1, "channel": 23, "enable": lora, "mode": "MASTER", "groupId": "novad101"}
    data["gps"] = {"enable": False}
    data["compatibility"] = {"supportLoraInfo": True}

    flag = sendSetCommand(self, Constant.WHAT_NET_TIMING, 0, Constant.ACTION_SET, 0, data=data, describe="setNTPModel")
    return flag
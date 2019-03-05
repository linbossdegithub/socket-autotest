#coding=utf8
'''
Created on 2018.10.31
@author: chenyongfa
'''


from constant.constant import Constant
from utils.common.common import  sendSetCommand


def setScreenPowerModel_MANUALLY(self):
    '''
             设置开关屏的模式为 手动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setScreenPowerModel_MANUALLY(self)
    '''
    data = {}
    data["type"] = "SCREENPOWER"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["mode"] = "MANUALLY"

    flag = sendSetCommand(self,Constant.WHAT_SCREEN_POWER,Constant.TYPE_MODE,Constant.ACTION_SET,0,data=data,describe="changeScreenPowerModel_MANUALLY")
    return flag



def setScreenPowerModel_AUTO(self):
    '''
             设置开关屏的模式为 自动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setScreenPowerModel_AUTO(self)
    '''

    data = {}
    data["type"] = "SCREENPOWER"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["mode"] = "AUTO"

    flag = sendSetCommand(self, Constant.WHAT_SCREEN_POWER, Constant.TYPE_MODE, Constant.ACTION_SET, 0,data=data,describe="changeScreenPowerModel_AUTO")
    return flag


#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''


from constant.constant import Constant
from utils.common.common import sendSetCommand


def setBrightnessModel(self, model):
    '''
             设置亮度控制模式
    :parma    self  必须
    :parma    model  控制模式 手动:MANUALLY 自动：AUTO
    :return    flag    bool型
    :example    flag = setBrightnessModel(self, 'AUTO')
    '''

    data = {}
    data["type"] = "SCREEN_BRIGHTNESS"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["mode"] = model

    flag = sendSetCommand(self, Constant.WHAT_SCREEN_BRIGHTNESS, Constant.TYPE_MODE,
                          Constant.ACTION_SET, 0, data=data, describe="setBrightnessModel:" + model)
    return flag


def setBrightness_AUTO(self):
    '''
             设置亮度控制模式为 自动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setBrightness_AUTO(self)
    '''

    flag = setBrightnessModel(self, 'AUTO')
    return flag


def setBrightness_MANUALLY(self):
    '''
             设置亮度控制模式为 手动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setBrightness_MANUALLY(self)
    '''

    flag = setBrightnessModel(self, 'MANUALLY')
    return flag

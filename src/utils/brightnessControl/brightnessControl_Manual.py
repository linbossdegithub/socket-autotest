#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

from utils.common.common import sendSetCommand
from constant.constant import Constant


def setBrightness_Manual(self, ratio):
    '''
    手动设置亮度
    :param self:
    :param ratio: 音量百分比
    :return: flag 是否成功
    :example    flag = setBrightness_Manual(self, ratio=50)
    '''

    data = {}
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["ratio"] = ratio
    print data
    flag = sendSetCommand(self, Constant.WHAT_SCREEN_BRIGHTNESS, Constant.TYPE_MANUAL,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setBrightness_Manual")
    return flag

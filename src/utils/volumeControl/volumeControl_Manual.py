#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

from utils.common.common import sendSetCommand
from constant.constant import Constant


def setVolume_Manual(self, ratio):
    '''
    手动设置音量
    :param self:
    :param ratio: 音量百分比
    :return: flag 是否成功
    :example    flag = setVolume_Manual(self, ratio=50)
    '''

    data = {}
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["ratio"] = ratio
    flag = sendSetCommand(self, Constant.WHAT_VOLUME, 0,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setVolume_Manual")
    return flag


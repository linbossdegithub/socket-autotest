#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

from constant.constant import Constant
from utils.common.common import sendGetCommand


def getBrightnessInfo(self):
    '''
    获取亮度相关配置信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：ratio
    :example    result = getBrightnessInfo(self)
    '''
    result = sendGetCommand(self, Constant.WHAT_SCREEN_BRIGHTNESS, Constant.TYPE_MANUAL,
                            Constant.ACTION_GET, 0, describe="getBrightnessInfo")
    return result


def getENVBrightnessInfo(self):
    '''
    获取环境亮度相关配置信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：ratio
    :example    result = getENVBrightnessInfo(self)
    '''
    result = sendGetCommand(self, Constant.WHAT_ENV_BRIGHTNESS, 0,
                            Constant.ACTION_GET, 0, describe="getENVBrightnessInfo")
    return result


def assertBrightnessInfo(self, result, ratio):
    '''
    判读亮度信息与预期的是否一致
    :param    self    必须
              result    字典    get命令返回的data结果
              ratio     float   音量百分比
    :example  assertBrightnessInfo(self, result, ratio=60.0)
    '''

    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
            flag = False
            print i+":"+str(li)
        else:
            if ratio and li["ratio"] != ratio:
                flag = False
                print i+":"+str(li["ratio"])
    self.assertTrue(flag, "亮度与预期不一致")

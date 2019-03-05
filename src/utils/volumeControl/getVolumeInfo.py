#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

from constant.constant import Constant
from utils.common.common import sendGetCommand


def getVolumeInfo(self):
    '''
             获取音量相关配置信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：ratio
    :example    result = getVolumeInfo(self)
    '''
    result = sendGetCommand(self, Constant.WHAT_VOLUME, 0,
                            Constant.ACTION_GET, 0, describe="getVolumeInfo")
    return result


def assertVolumeInfo(self, result, ratio):
    '''
    判读音量信息与预期的是否一致
    :param    self    必须
              result    字典    get命令返回的data结果
              ratio     float   音量百分比
    :example  assertVolumeInfo(self, result, ratio=60.0)
    '''

    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR,Constant.FAILED]:
            flag = False
            print i+":"+str(li)
        elif li == Constant.NOAPPLY:
            print i+":"+str(li)
        else:
            if ratio and li["ratio"] != ratio:
                flag = False
                print i + ":" + str(li)
    self.assertTrue(flag, "音量与预期不一致")

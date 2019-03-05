#coding=utf8
'''
Created on 2018.12.5
@author: gaowei
'''

from constant.constant import Constant
from utils.common.common import sendGetCommand


def getSysResolution(self):
    '''
            获取内部源分辨率信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：state（'OPEN' or 'CLOSE'）
    :example    result = getSysResolution(self)
    '''
    data = {"displayMode": 1}
    result = sendGetCommand(self, Constant.WHAT_SYS_ADVANCED, Constant.TYPE_CURRENT_RESOLUTION,
                            Constant.ACTION_GET, 0, data=data, describe="getSysResolution",
                            applyTo=["T1-4G", "T2-4G"])
    return result

def getCustomResolution(self):
    '''
            获取自定义分辨率信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：state（'OPEN' or 'CLOSE'）
    :example    result = getCustomResolution(self)
    '''
    data = {"displayMode": 1}
    result = sendGetCommand(self, Constant.WHAT_SYS_ADVANCED, Constant.TYPE_CURRENT_RESOLUTION,
                            Constant.ACTION_GET, 0, data=data, describe="getCustomResolution",
                            applyTo=["T1", "T2", "T3", "T4", "T6", "T8"])
    return result

def getHdimResolution(self):
    '''
            获取HDMI分辨率信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：state（'OPEN' or 'CLOSE'）
    :example    result = getHdimResolution(self)
    '''
    result = sendGetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_EDID,
                            Constant.ACTION_GET, 0, describe="getHdimResolution",
                            applyTo=["T2", "T2-4G", "T4", "T6", "T8"])
    return result


def assertResolutionInfo(self, result, width=None, height=None, resolutionValue=None):
    '''
    内部分辨率与预期的是否一致
    :param    self    必须
              result    字典    get命令返回的data结果
              resolutionValue     String   分辨率的值
    :example  assertSysResolutionInfo(self,result, resolutionValue=None)
    '''
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR, Constant.FAILED]:
            flag = False
            print i+":"+str(li)
        elif li == Constant.NOAPPLY:
            print i + ":" + str(li)
        else:
            if resolutionValue and li["value"] != resolutionValue:
                flag = False
                print i + ":" + str(li)
            else:
                if width and height and li["value"] != str(width) + 'x' + str(height) + 'p-60':
                    flag = False
                    print i + ":" + str(li)
    self.assertTrue(flag, "内部分辨率配置项与预期不一致")


def assertHdmiResolutionInfo(self, result, width=None, height=None):
    '''
           HDMI分辨率与预期的是否一致
    :param self    必须
    :param result  字典    get命令返回的data结果
    :param width: 显示屏宽度
    :param height: 显示屏高度
    :example  assertHdmiResolutionInfo(self,result, width=None, height=None)
    '''
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR, Constant.FAILED]:
            flag = False
            print i+":"+str(li)
        elif li == Constant.NOAPPLY:
            print i+":"+str(li)
        else:
            if width and li["width"] != width:
                flag = False
                print i + ":" + str(li)
            if height and li["height"] != height:
                flag = False
                print i + ":" + str(li)
    self.assertTrue(flag, "HDMI分辨率配置项与预期不一致")

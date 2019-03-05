#coding=utf8
'''
Created on 2018.12.5
@author: gaowei
'''

from constant.constant import Constant
from utils.common.common import sendGetCommand


def getVideoInfo(self):
    '''
             获取视频源相关配置信息
    :parma    self  必须
    :return    result  字典      key：sn号      value：state（'OPEN' or 'CLOSE'）
    :example    result = getVideoInfo(self)
    '''
    result = sendGetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                            Constant.ACTION_GET, 0, describe="getVideoInfo",
                            applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return result


def assertVideoInfo(self, result, videoMode=None, videoSource=None,
                    offsetX=None, offsetY=None,isScale=None):
    '''
    判读视频源信息与预期的是否一致
    :param    self    必须
              result    字典    get命令返回的data结果
              videoMode     int   模式，HDMI优先 0，手动 1， 定时 2  期望值
              videoSource   int   视频源 SOURCE_INSIDE 内部 0， SOURCE_HDMI HDMI 1
              offsetX     int   偏移X
              offsetY     int   偏移Y
              isScale   boolean   是否缩放，true为全屏缩放，false为不缩放
    :example  assertVideoInfo(self, result, videoMode=0, videoSource=1,
                    offsetX=10, offsetY=10,isScale=True)
    '''
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR, Constant.FAILED]:
            flag = False
            print i + ":" + str(li)
        elif li == Constant.NOAPPLY:
            print i + ":" + str(li)
        else:
            if videoMode and li["videoMode"] != videoMode:
                flag = False
                print i + ":" + str(li)
            if videoSource and li["videoSource"] != videoSource:
                flag = False
                print i + ":" + str(li)
            if offsetX and li["offsetX"] != offsetX:
                flag = False
                print i + ":" + str(li)
            if offsetY and li["offsetY"] != offsetY:
                flag = False
                print i + ":" + str(li)
            if isScale and li["isScale"] != isScale:
                flag = False
                print i + ":" + str(li)
    self.assertTrue(flag, "视频源配置项与预期不一致")

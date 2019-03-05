#coding=utf8
'''
Created on 2018.12.5
@author: gaowei
'''


from constant.constant import Constant
from utils.common.common import sendSetCommand


def setVideoControl_MANUALLY(self):
    '''
             设置视频源控制模式为 手动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setVideoControl_MANUALLY(self)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 1

    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data,describe="setVideoControl_MANUALLY",
                          applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag



def setVideoControl_AUTO(self):
    '''
             设置视频源控制模式为 自动
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setVideoControl_AUTO(self)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 2

    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data, describe="setVideoControl_AUTO",
                          applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag

def setVideoControl_HDMI_Priority(self):
    '''
             设置视频源控制模式为 HDMI优先
    :parma    self  必须
    :return    flag    bool型
    :example    flag = setVideoControl_hdmi_priority(self)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 0

    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data, describe="setVideoControl_HDMI_Priority",
                          applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag


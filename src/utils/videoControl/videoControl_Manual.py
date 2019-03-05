#coding=utf8
'''
Created on 2018.12.06
@author: gaowei
'''

from utils.common.common import jointArgument, getPacket, sendSetCommand
from constant.constant import Constant


def setInnerSource_Manual(self, offsetX=-1, offsetY=-1):
    '''
    设置内部源相关配置
    :param self:
    :param offsetX: 偏移X
    :param offsetY: 偏移Y
    :return: flag 是否成功
    :example    flag = setInnerSource_Manual(self, offsetX=10, offsetY=10)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 1
    data["videoSource"] = 0  # 内部
    if offsetX != -1:
        data["offsetX"] = offsetX
    if offsetY != -1:
        data["offsetY"] = offsetY
    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setInnerSource_Manual", applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag


def setHDMISource_Manual(self, offsetX=-1, offsetY=-1, isscale=None):
    '''
    设置HDMI源相关配置
    :param self:
    :param offsetX: 偏移X
    :param offsetY: 偏移Y
    :param isScale: 是否缩放，true为全屏缩放，false为不缩放
    :return: flag 是否成功
    :example    flag = setHDMISource_Manual(self, offsetX=10, offsetY=10,
                    isScale=True)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 1
    data["videoSource"] = 1  # HDMI
    if offsetX != -1:
        data["offsetX"] = offsetX
    if offsetY != -1:
        data["offsetY"] = offsetY
    if isscale:
        data["isScale"] = isscale
    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setHDMISource_Manual", applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag

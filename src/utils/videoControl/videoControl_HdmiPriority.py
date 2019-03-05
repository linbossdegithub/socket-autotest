#coding=utf8
'''
Created on 2018.12.06
@author: gaowei
'''

from utils.common.common import jointArgument, getPacket, sendSetCommand
from constant.constant import Constant


def setvideoInfo_HDMIPriority(self, offsetX=-1, offsetY=-1, isScale=None):
    '''
    设置HDMI源相关配置
    :param self:
    :param offsetX: 偏移X
    :param offsetY: 偏移Y
    :param isScale: 是否缩放，true为全屏缩放，false为不缩放
    :return: flag 是否成功
    :example    flag = setvideoInfo_HDMIPriority(self, offsetX=10, offsetY=10,
                    isScale=True)
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 0  # HDMI优先
    if offsetX != -1:
        data["offsetX"] = offsetX
    if offsetY != -1:
        data["offsetY"] = offsetY
    if isScale:
        data["isScale"] = isScale
    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setvideoInfo_HDMIPriority", applyTo=["T2-4G", "T2", "T4", "T6", "T8"])
    return flag

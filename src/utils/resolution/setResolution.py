# encoding=utf-8
'''
Created on 2018.12.06
@author: gaowei
'''

from utils.common.common import sendSetCommand
from constant.constant import Constant


def setCurrentResolution(self, resolutionValue):
    '''
        设置系统分辨率
    :param self:
    :param resolutionValue: 分辨率的值
    :return: flag 是否成功
    '''

    # 设置系统分辨率
    data_cus = {}
    data_cus["displayMode"] = 1  # 默认 DISPLAY_INTERFACE_TV
    data_cus["resolutionValue"] = resolutionValue
    flag = sendSetCommand(self, Constant.WHAT_SYS_ADVANCED, Constant.TYPE_CURRENT_RESOLUTION,
                          Constant.ACTION_SET, 0, data=data_cus,
                          describe="setCurrentResolution",
                          applyTo=["T2-4G", "T1-4G"])

    return flag


def setCustomResolution(self, width, height):
    '''
        设置自定义分辨率
    :param self:
    :param width: 显示屏宽度
    :param height: 显示屏高度
    :return: flag 是否成功
    '''
    # 设置自定义分辨率
    data_cus = {}
    data_cus["width"] = width
    data_cus["height"] = height
    data_cus["displayMode"] = 1  # 默认 DISPLAY_INTERFACE_TV
    flag = sendSetCommand(self, Constant.WHAT_SYS_ADVANCED, Constant.TYPE_CUSTOM_RESOLUTION,
                          Constant.ACTION_SET, 0, data=data_cus,
                          describe="setCustomResolution",
                          applyTo=["T1", "T2", "T3", "T4", "T6", "T8"])
    return flag


def setHDMIResolution(self, width, height):
    '''
        设置HDMI分辨率
    :param self:
    :param width: 显示屏宽度
    :param height: 显示屏高度
    :return: flag 是否成功
    '''
    # 设置HDMI分辨率
    data_cus = {}
    data_cus["width"] = width
    data_cus["height"] = height
    data_cus["fieldRate"] = 50  # 场频，即刷新频率 默认50
    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_EDID,
                          Constant.ACTION_SET, 0, data=data_cus,
                          describe="setHDMIResolution",
                          timeout=10,
                          applyTo=["T2", "T2-4G", "T4", "T6", "T8"])
    return flag

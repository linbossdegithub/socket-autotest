#coding=utf8
'''
Created on 2018.12.5
@author: gaowei
'''


from constant.constant import Constant
from utils.common.common import sendSetCommand, getCron


def setVideoInfo_Auto(self, offsetX=-1, offsetY=-1,
                    isScale=None, inside=None, hdmi=None):
    '''
    设置自定义分辨率
    :param self:
    :param isScale: 是否缩放，true为全屏缩放，false为不缩放
    :param offsetX: 偏移X
    :param offsetY: 偏移Y
    :param inside:object	内部源任务列表
                    cron	String	cron表达式，用户表示开始时间和重复
                    source	int	视频源 SOURCE_INSIDE 内部 0, SOURCE_HDMI HDMI 1
                    enable	boolean	该条定时任务是否生效
    :param hdmi:object	    hdmi任务列表
                    cron	String	cron表达式，用户表示开始时间和重复
                    source	int	视频源 SOURCE_INSIDE 内部 0, SOURCE_HDMI HDMI 1
                    enable	boolean	该条定时任务是否生效
    :return: flag 是否成功
    :example    flag = setVideoInfo_Auto(self, offsetX=10, offsetY=10,
                    isScale=True, inside=[['4,5,6,7', time, True]],
                    hdmi=[['0', time, True]])
    '''

    data = {}
    data["type"] = "VIDEO_CONTROL"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["videoMode"] = 2  # 定时
    if offsetX != -1:
        data["offsetX"] = offsetX
    if offsetY != -1:
        data["offsetY"] = offsetY
    if isScale:
        data["isScale"] = isScale
    conditions = []
    if inside:
        conditions = get_conditions(Constant.SOURCE_INSIDE, inside)
    if hdmi:
        conditions = get_conditions(Constant.SOURCE_HDMI, hdmi, conditions)
    if conditions:
        data["conditions"] = conditions
    print data
    flag = sendSetCommand(self, Constant.WHAT_VIDEO_CONTROL, Constant.TYPE_VIDEO_CONTROL,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setVideoInfo_Auto", applyTo=["T2-4G", "T2", "T4", "T6", "T8"])

    return flag


def get_conditions(type_source, source_list, conditions=[]):
    '''
        获取定时任务列表
    '''

    # 生成定时任务
    for cron_item in source_list:
        cron, flag = getCron(cron_item)
        con_item = {}
        con_item['cron'] = cron
        con_item['source'] = type_source
        con_item['enable'] = flag
        conditions.append(con_item)
    return conditions


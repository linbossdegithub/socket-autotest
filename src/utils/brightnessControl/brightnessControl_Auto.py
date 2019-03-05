#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

import time
from constant.constant import Constant
from utils.common.common import sendSetCommand, getCron


def setBrightnessInfo_Auto(self, timing_list=None, auto_list=None):
    '''
    设置亮度调节方案
    :param self:
    :param timing_list: object	定时任务列表
                        type	number	1：定时调节
                        cron    string array 重复次数，每条条件使用cron表达式数组表示，当为数组时，cron表达式之间使用或的关系
                        args	object	亮度调节参数，定时调试时args为亮度百分比
                        startTime  string  策略有效期开始时间yyyy-MM-dd HH:mm:ss
                        endTime    string  策略有效期结束时间yyyy-MM-dd HH:mm:ss ，永久有效的时间为4016-06-06 23:59:59
    :param auto_list:   object	自动任务列表
                        type    number	2：自动调节
                        cron    string array 重复次数，每条条件使用cron表达式数组表示，当为数组时，cron表达式之间使用或的关系
                        args    object	自动调节时args为自动调节参数
                                格式: "args":[maxEnvBrightness,minEnvBrightness,maxScreenBrightness,minScreenBrightness,segmentCount]
                        startTime  string  策略有效期开始时间yyyy-MM-dd HH:mm:ss
                        endTime    string  策略有效期结束时间yyyy-MM-dd HH:mm:ss ，永久有效的时间为4016-06-06 23:59:59
    :return: flag 是否成功
    :example    flag = setVideoInfo_Auto(self, offsetX=10, offsetY=10,
                    isScale=True, inside=[['4,5,6,7', time, True]],
                    hdmi=[['0', time, True]])
    '''

    data = {}
    data["type"] = "BRIGHTNESS"
    source = {}
    source["type"] = 0
    source["platform"] = 1
    data["source"] = source
    data["enable"] = True

    # 当前数据的时间戳，为后期可能使用
    data["timeStamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取条件集合
    conditions = []
    segmentconfig = {}
    if timing_list:
        conditions = get_timeconditions(timing_list, conditions)
    # if auto_list:
    #     conditions, segmentconfig = get_autoconditions(auto_list, conditions)
    data["conditions"] = conditions
    if segmentconfig:
        data["segmentconfig"] = segmentconfig
    print data
    flag = sendSetCommand(self, Constant.WHAT_SCREEN_BRIGHTNESS, Constant.TYPE_POLICY,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setBrightnessInfo_Auto")

    return flag


def get_timeconditions(source_list, conditions=[]):
    '''
        获取定时任务列表
    '''

    # 生成定时任务
    for cron_item in source_list:
        cron, flag = getCron(cron_item)
        con_item = {}
        con_item['cron'] = [cron]
        con_item['enable'] = flag
        con_item['type'] = 1
        con_item['args'] = [cron_item[3]]
        con_item["startTime"] = cron_item[4]
        con_item["endTime"] = cron_item[5]
        conditions.append(con_item)
    return conditions

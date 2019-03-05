#coding=utf8
'''
Created on 2018.12.17
@author: gaowei
'''

from utils.common.common import sendSetCommand, getCron
from constant.constant import Constant


def setVolume_Auto(self, condition_list=[]):
    '''
    自动设置音量
    :param self:
    :param conditions: 按照条件执行的任务集合，我们支持多个任务。
    :return: flag 是否成功
    :example    flag = setVolume_Auto(self, condition_list=[['0', time, True, '60.0',
                                     '2017-09-01 00:00:00', '4016-06-06 24:00:00']])
    '''

    data = {}
    data["type"] = "VOLUME"
    source = {}
    source["type"] = 0
    source["platform"] = 4
    data["source"] = source
    data["enable"] = True
    conditions = get_conditions(condition_list)
    data["conditions"] = conditions
    print data
    flag = sendSetCommand(self, Constant.WHAT_VOLUME, Constant.TYPE_POLICY,
                          Constant.ACTION_SET, 0, data=data,
                          describe="setVolume_Auto")
    return flag


def get_conditions(condition_list):
    '''
    获取定时任务列表
    '''
    # 生成定时任务
    conditions = []
    for con in condition_list:
        con_item = {}
        cron, flag = getCron(con)
        con_item["cron"] = [cron]
        con_item["value"] = con[3]
        con_item["enable"] = flag
        con_item["startTime"] = con[4]
        con_item["endTime"] = con[5]
        conditions.append(con_item)

    return conditions

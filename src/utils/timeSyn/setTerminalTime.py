#coding=utf8
'''
Created on 2018.11.29
@author: chenyongfa
'''
import time
from datetime import datetime

from constant.constant import Constant
from utils.common.common import sendSetCommand



def setTerminalTime(self,timestr = '2018-01-01 00:00:00'):
    '''
    设置终端的时间
    :param    self      必须
    :param    timestr   格式化的时间字符串，如需另传时间 一定要按照默认值的格式
    :return   flag   bool型
    :example  flag = setTerminalTime(self)
    '''

    data = {}
    local_datetime = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    time_num = long(time.mktime(local_datetime.timetuple()) * 1000.0)
    data["utcTimeMillis"] = time_num
    data["timeZone"] = "Asia/Shanghai"
    data["gmt"] = "GMT+08:00"
    data["isTimeOffsetEnable"] = False
    data["beginTime"] = ""
    data["endTime"] = ""
    data["timeOffsetValue"] = 0
    flag = sendSetCommand(self,Constant.WHAT_TIME_ZONE,0, Constant.ACTION_MODIFY,0,data=data,timeout=5,describe="setTerminalTime")
    return flag


#coding=utf8
'''
Created on 2018.10.16
@author: chenyongfa
'''

from utils.common.common import jointArgument, getPacket, sendSetCommand
from constant.constant import Constant



def closeScreenManual(self):
    '''
             手动关屏
    :parma    self  必须
    :return    flag    bool型 （命令是否发送成功）
    :example    flag = closeScreenManual(self)
    '''

    data = {"type": "SCREENPOWER", "source": {"type": 1, "platform": 1}, "state": "CLOSE"}
    flag = sendSetCommand(self, Constant.WHAT_SCREEN_POWER, Constant.TYPE_MANUAL, Constant.ACTION_SET, 0, data=data,
                          describe="openScreen")
    return flag


def openScreenManual(self):
    '''
             手动开屏
    :parma    self  必须
    :return    flag    bool型 （命令是否发送成功）
    :example    flag = openScreenManual(self)
    '''
    data = {"type":"SCREENPOWER","source":{"type":1,"platform":1},"state":"OPEN"}
    flag = sendSetCommand(self,Constant.WHAT_SCREEN_POWER,Constant.TYPE_MANUAL,Constant.ACTION_SET,0,data=data,describe="openScreen")
    return flag






    
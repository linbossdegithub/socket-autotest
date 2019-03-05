#coding=utf8
'''
Created on 2018.11.5
@author: chenyongfa
'''

from constant.constant import Constant
from utils.common.common import sendGetCommand



def getScreenPowerState(self):
    '''
             获取屏体的开关屏状态
    :parma    self  必须
    :return    result  字典      key：sn号      value：state（'OPEN' or 'CLOSE'）
    :example    result = getScreenPowerState(self)
    '''
    result = sendGetCommand(self,Constant.WHAT_SCREEN_POWER,Constant.TYPE_MANUAL,Constant.ACTION_GET,0,describe="getScreenPowerState")
    return result

def assertPowerState(self,result,state):
    '''
    断言开关屏状态与预期的是否一致
    :param    self    必须
              result    字典    get命令返回的data结果
              state    字符串   "OPEN" or "CLOSE"  期望值
    :example  assertCareResult(self,result,"OPEN")
    '''
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
            flag = False
            print i+":"+str(li)
        else:
            if (li["state"] != state.upper()):
                flag = False
                print i + ":" + str(li)
    self.assertTrue(flag,"某些屏体开关屏状态与预期不一致")
    
    
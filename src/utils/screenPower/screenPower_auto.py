#coding=utf8
'''
Created on 2018.10.16
@author: chenyongfa
'''

from constant.constant import Constant
from utils.common.common import getCron,  sendSetCommand


def openCloseScreenAuto(self,open=[],close=[]):
    '''
            设置自动开关屏策略
    :param1   self    必须
    :param2   open    二维列表     外层表示有N条策略，内层是每条策略的具体内容
                                                                 内层列表    第一位【 0：每天    1：周日    2：周一    3：周二    ... 7:周六     "1,2,3":周日/周一/周二 】
                                                                                     第二位  字符串   eg:: "15:16":15点16分       "15:16:17":15点16分17秒
                                                                                     第三位  bool型     Ture 或者   False
    :param3  close   同上
    :return  flag bool型   是否下发成功   
    :example flag = openCloseScreenAuto(self,open=[[0,'15:20',True],[]],close=[["1,2","14:20:45",False]])
                    
    '''
    conditions = []
    if open:
        cron_open = {}
        for li in open:
            cron, flag = getCron(li)
            cron_open["cron"] = [cron]
            cron_open["action"] = "OPEN"
            cron_open["enable"] = flag
            conditions.append(cron_open)
    if close:
        cron_close = {}
        for li in close:
            cron, flag = getCron(li)
            cron_close["cron"] = [cron]
            cron_close["action"] = "CLOSE"
            cron_close["enable"] = flag
            conditions.append(cron_close)

    source = {}
    source["type"] = 0
    source["platform"] = 1

    data = {}
    data["type"] = "SCREENPOWER"
    data["source"] = source
    data["enable"] = True
    data["conditions"] = conditions

    # print data
    flag = sendSetCommand(self,Constant.WHAT_SCREEN_POWER,Constant.TYPE_POLICY,Constant.ACTION_SET,0,data=data,describe='openCloseScreenAuto')
    return flag





        
    
    

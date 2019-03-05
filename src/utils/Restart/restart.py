#encoding=utf-8
'''
Created on 2018年11月1日

@author: linhuajian
'''
import time
import datetime
from constant.constant import Constant
from utils.login.search_login import searchT
from utils.login.search_login import logIns, logout
from utils.common.common import getCron, sendSetCommand, getAllKey
from utils.common.getPictureType import getPictureType
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def restart_CONDITIONS(self,conditions=[]):
    '''
            设置自动重启策略
    :param1   self        必须
    :param2   conditions  二维列表     外层表示有N条策略，内层是每条策略的具体内容
                                                                             内层列表    第一位【 0：每天    1：周日    2：周一    3：周二    ... 7:周六     "1,2,3":周日/周一/周二 】
                                                                                                 第二位  字符串   eg:: "15:16":15点16分       "15:16:17":15点16分17秒
                                                                                                 第三位  bool型     Ture 或者   False
    :return  flag bool型   是否下发成功   
    :example flag = restart_CONDITIONS(self,conditions=[[0,'15:20',True],["2,3",'16:20',False]])                 
'''    
    conditions_temp = []
    for i in range(len(conditions)):
        li = {}
        cron,flag = getCron(conditions[i])
        li["cron"] = [cron]
        li["enable"] = flag
        conditions_temp.append(li)
    source ={"type":0,"platform":1}
    data={'type':"REBOOT",'source':source,'executionType':"BY_CONDITIONS",'reason':"Just to test",'conditions':conditions_temp}
        
    flag = sendSetCommand(self,Constant.WHAT_SYS_ADVANCED,Constant.TYPE_REBOOT,Constant.ACTION_SET,0,data=data,timeout=1,describe="set_restart")
    return flag


def restart_IMMEDIATELY(self):
    '''
            手动立即重启
    :param1   self        必须
    :return  flag bool型   是否下发成功   
    :example flag = restart_IMMEDIATELY(self)
                    
    '''
    source ={"type":0,"platform":1}
    data={"type":"REBOOT","source":source,"executionType":"IMMEDIATELY","reason":"Just to test","conditions":[]}
    flag = sendSetCommand(self,Constant.WHAT_SYS_ADVANCED,Constant.TYPE_REBOOT,Constant.ACTION_SET,0,data=data,timeout=5,describe="restart_IMMEDIATELY")
    return flag


def assert_restartResult(self,timeout=60):
    '''
            判断重启是否成功
    :param1   self        必须
    :param2   sleep     type : int 最大等待重启时间 
    :return  flag bool型   在最大等待时间内是否重启成功
    :example flag = assert_restartResult(self,sleep=240)
                    
    '''
    sns = getAllKey("searchRes")
    result = {}
    for sn in sns:
        result[sn] = 0
    i = 0
    while True:
        searchT(self)
        search_sns = self.searchRes.keys()
        for sn in sns[:]:
            if sn not in search_sns:
                result[sn] += 2
                try:
                    sns.remove(sn)
                except ValueError:
                    print "搜到其他卡："+sn
        print sns
        if not sns:
            break
        i+=1
        # time.sleep(1)
        if i>15:
            break
    print "============================="
    time.sleep(10)
    n = 0
    sns1 = getAllKey("searchRes")
    print sns1
    while True:
        searchT(self)
        search_sns = self.searchRes.keys()

        for sn in sns1[:]:
            if sn in search_sns:
                result[sn] += 1
                try:
                    sns1.remove(sn)
                except ValueError:
                    print "搜到其他卡："+sn
        print sns1
        if not sns1:
            break
        time.sleep(3)
        n+=3
        if n>timeout-10:
            break
    flag = True
    for sn in result.keys():
        if result[sn] != 3:
            flag = False
            print sn +"restart failed："+ str(result[sn])
    return flag

    
    
    
    
    

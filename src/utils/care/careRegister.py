#coding=utf8
'''
Created on 2018.10.30
@author: chenyongfa
'''
import time

from constant.constant import Constant
from utils.common.common import sendSetCommand


def careRegister(self,url,username):
    '''
            将等陆的终端注册至指定的节点和用户下
    :param    self    必须
              url    字符串    eg：care.novaicare.com  注意不用写"http：//"
              username    字符串    care的用户名
    :return   flag   bool型
    :example  flag = careRegister(self,"10.20.8.161","chenyongfa")
    '''
    data = {}
    data["state"] = True
    data['url'] = url
    data['username'] = username
    flag = True
    for sn in self.sns:
        flag1 = sendSetCommand(self, Constant.WHAT_MONITOR, Constant.TYPE_CARE, Constant.ACTION_SET, 0, data=data, sns=[sn], timeout=20, describe="registerCare")
        if not flag1:
            flag = False
        else:
            print sn + "注册care命令发送成功"
        # time.sleep(3)

    # n = len(self.sns)/4
    # for i in range(n+1):
    #     flag1 = sendSetCommand(self,Constant.WHAT_MONITOR,Constant.TYPE_CARE,Constant.ACTION_SET,0,data=data,sns=(self.sns)[i*4:(i+1)*4],timeout=20,describe="registerCare")
    #     if not flag1:
    #         flag = False
    #     time.sleep(3)

    return flag


#coding=utf8
'''
Created on 2018.12.11
@author: chenyongfa
'''
from constant.constant import Constant
from utils.common.common import sendGetCommand, getConf


# def getVersion(self):
#     data = {}
#     data["packageName"] = ["nova.priv.terminal.syssetting","nova.priv.terminal.screen"]
#     result = sendGetCommand(self,Constant.WHAT_VERSION,Constant.TYPE_INSTALLED_PACKAGEINFOS,Constant.ACTION_GET,0,data=data,describe="获取终端版本号")
#     return result

def getFireWareVersion(self):
    result = sendGetCommand(self, Constant.WHAT_VERSION, Constant.TYPE_FIREWARE, Constant.ACTION_GET, 0,timeout=5,describe="获取终端固件版本号")
    return result

def assertAPPVersion(self):
    result = getFireWareVersion(self)
    version = getConf("data","appversion")
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
            print i + ":" + str(li)
            flag = False
        elif li["mainVersion"]!= version:
            flag = False
            print i + "的软件版本号与预期不相符:"+li["mainVersion"]
    self.assertTrue(flag,"终端存在与预期不相符的版本号")

def assertOSVersion(self):
    result = getFireWareVersion(self)
    version1 = getConf("data","os3368version").split("V")[1]
    version2 = getConf("data","os3128version").split("V")[1]
    flag = True
    for i in self.sns:
        li = result[i]
        v = li["model"].split("V")[1]
        if li in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
            print i + ":" + str(li)
            flag = False
        elif not ((version1==v) or (version2==v)):
            flag = False
            print i + "的系统版本号与预期不相符:"+str(li["model"])
    self.assertTrue(flag,"系统存在与预期不相符的版本号")

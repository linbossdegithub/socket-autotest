#coding=utf8
'''
Created on 2018.12.11
@author: chenyongfa
'''
import json
import os
import re

from constant.constant import Constant
from utils.common.common import sendSetCommand, setConf, getConf
from utils.common.fileOperation import getFileMd5
from utils.common.ftper import uploadFile


def update(self,type="",sns = None):
    if type == "APP":
        UPath = os.path.abspath("../file/update/APP")
        for i in os.listdir(UPath):
            if "UPDATE_APP" in i:
                filename = i
    elif type == "OS3128":
        UPath = os.path.abspath("../file/update/OS3128")
        for i in os.listdir(UPath):
            if "UPDATE_OS" in i:
                filename = i
    elif type == "OS3368":
        UPath = os.path.abspath("../file/update/OS3368")
        for i in os.listdir(UPath):
            if "UPDATE_OS" in i:
                filename = i
    else:
        raise RuntimeError("update方法的type参数有误")
    if not filename:
        print "升级文件目录下没有"+type+"升级包"
        return False

    filepath = UPath+"/"+filename
    source = "/cache/"+filename

    '''上传升级文件'''
    flag=uploadFile(self, user="supervisor",file=filepath,ftpdir="",sns=sns)

    if flag:
        print type+"升级文件全部上传成功"
    else:
        print type + "升级文件未全部上传成功"

    if type == "APP":
        version = re.findall(r"UPDATE_APP_(.+?).nuzip",filename)[0]
        setConf("data","appversion",version)
    elif type=="OS3128":
        version = re.findall(r"UPDATE_OS_(.+?).nuzip", filename)[0]
        setConf("data", "os3128version", version)
    elif type=="OS3368":
        version = re.findall(r"UPDATE_OS_(.+?).nuzip", filename)[0]
        setConf("data", "os3368version", version)

    size = os.path.getsize(filepath)
    md5 = getFileMd5(filepath)
    data = {}
    data["type"] = "UPDATE"
    data["source"] = {"type":0,"platform":1}
    tasks = []
    task = {}
    task["packageType"] = "NUZIP"
    task["version"] = version
    task["executionType"] = "IMMEDIATELY"
    if type=="APP":
        task["updateType"] = "UPDATE"
        task["startupAfterInstalled"] = True
        task["startupAfterBoot"] = True

    task["conditions"] = []
    task["source"] = source
    task["size"] = int(size)
    task["md5"] = md5

    tasks.append(task)
    data["tasks"] = tasks
    print data

    result = sendSetCommand(self,Constant.WHAT_UPDATE,0,Constant.ACTION_UPDATE,0,sns=sns,data=data,timeout=120,describe=type+"升级命令")
    return result


def updateAPP(self):
    """
    升级APP(注意：请将APP升级包放在工程src/file/update/APP 目录下)
    :param   self      必须
    :return  flag      是否全部升级成功   
    :return  version   要升级的版本号   
    :example flag,version =  updateAPP(self)
    """

    flag= update(self,type="APP")
    return flag

def updateOS(self):
    """
    升级OS(注意：请将OS升级包放在工程src/file/update/OS 目录下)
    :param   self      必须
    :return  flag      升级系统的命令是否全部成功下发，注意：不代表系统升级成功 
    :return  version   要升级的版本号
    :example flag,version =  updateOS(self)
    """
    sns_3368 = []
    sns_3128 = []
    for sn in self.sns:
        platform = json.loads(getConf("searchRes",sn))["platform"].encode()
        if "336" in platform:
            sns_3368.append(sn)
        elif "312" in platform:
            sns_3128.append(sn)
        else:
            raise RuntimeError("未知型号："+ platform)
    flag1 = True
    flag2 = True
    if sns_3368:
        print "shengji 3368"
        flag1= update(self,type="OS3368",sns=sns_3368)

    if sns_3128:
        print "shengji 3128"
        flag2= update(self, type="OS3128", sns=sns_3128)
    return flag1 and flag2




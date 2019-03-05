#coding=utf8
'''
Created on 2018.12.13
@author: chenyongfa
'''
from constant.constant import Constant
from utils.common.common import sendGetCommand


def getMd5(self,file):
    data = {}
    data["url"] =file
    result = sendGetCommand(self,Constant.WHAT_FILE,Constant.TYPE_MD5,Constant.ACTION_GET,0,data=data,timeout=5,describe="获取md5值")
    return result
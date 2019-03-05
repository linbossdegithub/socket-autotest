#coding=utf8
'''
Created on 2018.10.15
@author: chenyongfa
'''
import ConfigParser
import json
import os
import struct
import threading
import Queue
import datetime
import threading
import json
from copy import copy
from time import sleep


def jointArgument(param,type,action):
    '''
            将 param,type,action 三个参数按照协议组合成 param2
    :param  param  16进制
            type    16进制
            action   16进制
    :return  param2  int
    :example parma2 = jointArgument(0,0x44,0x22)
    '''
    return (0xff & action) | ((0xff & type) << 8) | ((0xffff & param) << 16)

def getPacket(flag = 0x4e4f5641,sequence=-1, type=0x5251, param1=0, param2=0, data=None, offset=0):
    '''
            将 协议中各参数组成字节流
    :param  data  字符串
                                    其他         16进制
    :return  buffer  bytearray(字节数组)
    :example buffer = getPacket(param1=0x55,param2=0,data="")
    '''
    if type>32767:
        type = -(65535-type)
    buffer = bytearray(struct.pack('iihhi',flag,sequence,type,param1,param2))
    count = 0
    if(data):
        count = len(bytearray(data))
        
    buffer[16:] = bytearray(struct.pack('ih',count,0))
    sum = 0
    for i in range(22):
        if buffer[i] > 127 :
            a = -(256-buffer[i])
        else:
            a = buffer[i]
        sum+=a
    buffer[22:] = bytearray(struct.pack('h',sum))
    if (data):
        buffer[24:] = bytearray(data)
    return buffer

def getAllKey(section):
    cp = ConfigParser.ConfigParser()
    if os.path.isfile("./terminal.conf"):
        cp.read("./terminal.conf")
    elif os.path.isfile("../terminal.conf"):
        cp.read("../terminal.conf")
    elif os.path.isfile("../../terminal.conf"):
        cp.read("../../terminal.conf")   
    else:
        raise Exception("wrong path of terminal.conf")
    keys = []
    for i in cp.items(section):
        keys.append(i[0])
    return keys
        

def getConf(section,option):

    if os.path.isfile("./terminal.conf"):
        path = "./terminal.conf"
    elif os.path.isfile("../terminal.conf"):
        path = "../terminal.conf"
    elif os.path.isfile("../../terminal.conf"):
        path = "../../terminal.conf"
    elif os.path.isfile("../../../terminal.conf"):
        path = "../../../terminal.conf"
    else:
        raise Exception("wrong path of terminal.conf")
    cp = ConfigParser.ConfigParser()
    cp.read(path)
    return cp.get(section, option)

def setConf(section, option, value):

    if os.path.isfile("./terminal.conf"):
        path = "./terminal.conf"
    elif os.path.isfile("../terminal.conf"):
        path = "../terminal.conf"
    elif os.path.isfile("../../terminal.conf"):
        path = "../../terminal.conf"
    elif os.path.isfile("../../../terminal.conf"):
        path = "../../../terminal.conf"
    else:
        raise Exception("wrong path of terminal.conf")
    cp = ConfigParser.ConfigParser()
    cp.read(path)
    cp.set(section, option, value)
    cp.write(open(path, "w"))

def removeSection(section):
    if os.path.isfile("./terminal.conf"):
        path = "./terminal.conf"
    elif os.path.isfile("../terminal.conf"):
        path = "../terminal.conf"
    elif os.path.isfile("../../terminal.conf"):
        path = "../../terminal.conf"
    else:
        raise Exception("wrong path of terminal.conf")
    cp = ConfigParser.ConfigParser()
    cp.read(path)
    cp.remove_section(section)
    cp.write(open(path, "w"))

def addSection(section):
    if os.path.isfile("./terminal.conf"):
        path = "./terminal.conf"
    elif os.path.isfile("../terminal.conf"):
        path = "../terminal.conf"
    elif os.path.isfile("../../terminal.conf"):
        path = "../../terminal.conf"
    else:
        raise Exception("wrong path of terminal.conf")
    cp = ConfigParser.ConfigParser()
    cp.read(path)
    cp.add_section(section)
    cp.write(open(path, "w"))

def removeData(section):
    cp = ConfigParser.ConfigParser()
    if os.path.isfile("./terminal.conf"):
        cp.read("./terminal.conf")
        keys = []
        for i in cp.items(section):
            keys.append(i[0])
        for i in keys:
            cp.remove_option(section, i)
        cp.write(open("./terminal.conf", "w"))
    elif os.path.isfile("../terminal.conf"):
        cp.read("../terminal.conf")
        keys = []
        for i in cp.items(section):
            keys.append(i[0])
        for i in keys:
            cp.remove_option(section, i)
        cp.write(open("../terminal.conf", "w"))
    elif os.path.isfile("../../terminal.conf"):
        cp.read("../../terminal.conf") 
        keys = []
        for i in cp.items(section):
            keys.append(i[0])
        for i in keys:
            cp.remove_option(section, i)
        cp.write(open("../../terminal.conf", "w"))  
    else:
        raise Exception("wrong path of terminal.conf")
    
    
def getCron(li):
    '''
            将一个数组转换成cron，并返回cron 和 传入的bool
    :param li   type:[]     eg：[0,"15:16:17",Ture] ["1,2,3","15:17",False]
    :return cron  type:str
            flag    type: bool
    :example cron,flag = getCron([0,15:16:17,Ture])
    '''
    cron = [0,0,0,"?","*",0]
    time = li[1].split(":")

    for i in range(len(time)):
        cron[2-i] = int(time[i])
    if str(li[0])=="0" :
        # cron[3] = "*"
        cron[5] = "*"
    else:
        # cron[3] = "?"
        cron[5] = li[0]
    cron = " ".join(str(x) for x in cron)
    return cron,li[2]


    
def assertResult(self,result,expect,describe):
    '''
            判断每个T卡的执行结果是否与预期的相符
    :param self    必须
    :param result  字典     所有T卡的执行结果  {sn：expect}
    :param expect    期望值
    :param describe  字符串  判断失败后输出的描述信息
    :return flag    type: bool
            
    :example flag = verifyResult(self,result,"OPEN")
    '''
    flag = True
    for i in self.sns:
        if result[i] != expect:
            flag = False
            break
    self.assertTrue(flag,describe)

def getNextTime(seconds=60,minutes=0,hours=0):
    '''
    在当前时间的基础上得到一个之前或者之后的时间
    :param seconds   在当前时间的基础上+n秒，支持正负值
    :param minutes   在当前时间的基础上+n分钟，支持正负值
    :param hours   在当前时间的基础上+n小时，支持正负值
    :return  time   字符串   %H:%M:%S 格式的时间 
    :example time  = getNextTime(self，seconds=60,minutes=0,hours=0)
    '''
    time = str((datetime.datetime.now() + datetime.timedelta(seconds=seconds,minutes=minutes,hours=hours)).strftime("%H:%M:%S"))
    return str(time)


def sendGetCommand(self,what,type, action,param,data=None,sns=None,timeout=3,describe="",applyTo=[]):
    '''
    发送获取类即有data返回的命令
    :param self    必须
    :param what  16进制数    socket所要发送的字节流数据
    :param type  16进制数    socket所要发送的字节流数据
    :param action  16进制数    socket所要发送的字节流数据
    :param param  16进制数    socket所要发送的字节流数据
    :param data    必须用字典    若无data，默认为None
    :param time    发送命令与获取返回值的间隔时间 默认2s
    :param describe  字符串  此命令的描述
    :param applyTo  列表  此命令适用的终端类型
    :return result    type: 字典   返回的data数据

    :example result = sendGetCommand(self,buffer,what,type, action,param,data=None,time=1,describe="注册")
    '''
    result = sendCommand(self, "GET", what, type, action, param, data=data, timeout=timeout,describe=describe, applyTo=applyTo)
    return result
    
    
def sendSetCommand(self,what,type, action,param,data=None,sns=None,timeout=5,describe="",applyTo=[]):
    '''
    发送设置类即无data返回的命令
    :param self    必须
    :param what  16进制数    socket所要发送的字节流数据
    :param type  16进制数    socket所要发送的字节流数据
    :param action  16进制数    socket所要发送的字节流数据
    :param param  16进制数    socket所要发送的字节流数据
    :param data    必须用字典    若无data，默认为None
    :param time    发送命令后获取返回值的超时时间 默认3s
    :param describe  字符串  此命令的描述
    :param applyTo  列表  此命令适用的终端类型
    :return flag    type: bool   所有命令是否成功发送

    :example flag = sendSetCommand(self,what,type, action,param,data=None,times=1,describe="注册")
    '''
    flag = sendCommand(self,"SET",what,type, action,param,data=data,sns=sns,timeout=timeout,describe=describe,applyTo=applyTo)
    return flag


def sendCommand(self,model,what,type, action,param,data=None,sns=None,timeout=3,describe="",applyTo=[]):
    '''
    发送获取类即有data返回的命令
    :param self    必须
    :param what  16进制数    socket所要发送的字节流数据
    :param type  16进制数    socket所要发送的字节流数据
    :param action  16进制数    socket所要发送的字节流数据
    :param param  16进制数    socket所要发送的字节流数据
    :param data    必须用字典    若无data，默认为None
    :param time    发送命令与获取返回值的间隔时间 默认2s
    :param describe  字符串  此命令的描述
    :param applyTo  列表  此命令适用的终端类型
    :return result    type: 字典   返回的data数据

    :example result = sendGetCommand(self,buffer,what,type, action,param,data=None,time=1,describe="注册")
    '''
    flag = True
    buffer1 = jointArgument(param, type, action)
    if data:
        data = json.dumps(data)
    buffer = getPacket(param1=what, param2=buffer1, data=data)
    sockets = self.sockets
    queues = self.queues
    if sns == None:
        sns = self.sns
    threads = []
    if model == "GET":
        result = {}
    elif model == "SET":
        flag = True
    else:
        raise RuntimeError("Model参数错误")
    for sn in sns:
        if applyTo:
            info = json.loads(getConf("searchRes",sn))
            productName = info["productName"]
            if not productName in applyTo:
                print sn +":型号为"+productName+", "+describe+"命令不适用"
                if model == "GET":
                    result[sn] = "NOAPPLY"
                continue
        def send(sn,timeout,flag):
            queues[sn].queue.clear()
            sockets[sn].sendall(buffer)
            try:
                response = queues[sn].get(timeout=timeout)
                res = bytearray(response)
                a = res[12]
                if a == 0:
                    # print sn + ": "+describe+" COMMAND SEND SUCCESS"
                    if model == "GET":
                        result[sn] = json.loads(str(res[24:]))
                else:
                    if model == "GET":
                        result[sn] = "FAILED"
                    if model == "SET":
                        flag = False
                    print sn + ": " + describe + " FAILED"+":"+str(a)
            except Queue.Empty:
                if model == "GET":
                    result[sn] = "ERROR"
                if model == "SET":
                    flag = False
                print sn +":"+describe+" 命令 未响应"

        t = threading.Thread(target=send, args=(sn,timeout,flag))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    if model == "GET":
        return result
    if model == "SET":
        return flag



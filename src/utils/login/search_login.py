#coding=utf-8
'''
Created on 2018.10.15
@author: chenyongfa
'''
import Queue
import json
import socket
import threading
import time
import unittest

from constant.constant import Constant 
from utils.common.common import getPacket, getConf, setConf, getAllKey, removeSection, addSection
from utils.common.heartThread import HeartThread
from utils.common.recThread import RecThread


def udp_send_data(buffer):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    s.bind((ip,Constant.UDP_TERMINAL_LISTEN_PORT))
    addr=('<broadcast>',Constant.UDP_TERMINAL_LISTEN_PORT)
    s.sendto(buffer,addr)
    s.close()
    
def udp_receive_data(self):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    s.settimeout(6)
    s.bind((ip, Constant.UDP_HAND_LISTEN_PORT))
    data = getConf("data","sn")
    if self:
        self.searchRes = {}
    if data :
        sns = data.split(",")
        while True:
            try:
                data, address = s.recvfrom(1024)
                a = data[24:]
                info = json.loads(a)
                info["addr"] = address[0]
                strn = json.dumps(info)
                sn = info["sn"].encode('utf-8').lower()
                for i in sns:
                    if i in sn:
                        if self:
                            self.searchRes[sn] = info
                        else:
                            setConf("searchRes",sn,strn)
                        sns.remove(i)
                        break
                if not sns:
                    return
            except socket.timeout:
                    s.close()
                    if sns:
                        if self:
                            return
                        print "未搜索到屏体：" + str(sns)
                        setConf("data","bad_sn",str(sns))
                    return
    else:
        while True:
            try:
                data, address = s.recvfrom(1024)
                a = data[24:]
                info = json.loads(a)
                info["addr"] = address[0]
                strn = json.dumps(info)
                sn = info["sn"].encode('utf-8').lower()
                if self:
                    self.searchRes[sn] = info
                else:
                    setConf("searchRes", sn, strn)
            except socket.timeout:
                    s.close()
                    return
        
def searchT(self=None):
    if not self:
        removeSection("searchRes")
        addSection("searchRes")
        setConf("data","bad_sn","")
        print "search and login terminal"
    buffer = getPacket(type=-30635,param1=0x81)
    t = threading.Thread(target=udp_receive_data,args=(self,))
    t.start()
    time.sleep(1)
    udp_send_data(buffer)
    t.join()
    if getConf("data","bad_sn"):
        return False
    else:
        return True

    
def TCP_receive_data(s,q):
    RecThread(socket=s,queue=q).start()
    
def getLoginBuffer(key):
    data = {}
    data["sn"] = key.upper()
    data["username"] = 'admin'
    data['password'] = getConf('constant', 'login_password')
    data['loginType'] = 0
    source = {}
    source['type'] = 1
    source['platform'] = 1
    data['source'] = source
    buffer = getPacket(sequence=-1,type=0x5251,param1=0x00,data=str(data))
    return buffer
    
    
def logIn(s,q,ip,key):
    s.connect((ip,Constant.TCP_SCREEN_SERVER_PORT))
    a= RecThread(queue=q,socket=s,key=key)
    a.start()
    buffer = getLoginBuffer(key)
    s.sendall(buffer)

        
def logins(self,timeout=3,tcpPort=Constant.TCP_SCREEN_SERVER_PORT):
    '''
            搜索并登陆局域网内所有或者指定的某几个异步终端,并将sockets,queues,sns,hearThreads实例赋给self
    :param self self.sockets      数组     包含所有建立的socket实例
                self.queuess      数组     包含所有建立的queue实例
                self.sns          数组     包含所有登陆的异步终端的sn号
                self.hearThreads  数组     包含所有心跳进程的实例
                self.searchRes   字典     {sn:{addr:value,logined:value}...}
                self.isLoginAll   bool    是否全部等绿成功
    :param timeout 登陆超时时间
    :param sn=[] 列表 元素可为数子或者字符串（sn号的一部分）
    :return  无
    :example logIns(self,["3305",3306]) 登陆sn号中包含3305 和 3306 的终端
             logIns(self) 登陆局域网内所有搜到的终端
    '''
    # searchT(self)
    # searchedSn = []
    # keys = list(self.searchRes.keys())
    # args = sn
    # if not args:
    #     args = keys
    # else:
    #     args = [str(li) for li in args]
    
    sockets = {}
    queues = {}
    sns = []
    hearThreads = []
    ts = []
    searchedSn = getAllKey("searchRes")
    for sn in searchedSn:
        res = json.loads(getConf("searchRes",sn))
        if res["logined"]:
            # print key+" logined ==FAILED==,already logined by others"
            continue
        def a(sn,res,timeout):
            ip = res["addr"]
            q = Queue.Queue()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip, tcpPort))
            RecThread(queue=q, socket=s, key=sn).start()
            time.sleep(0.5)
            buffer = getLoginBuffer(sn)
            s.sendall(buffer)
            try:
                res = q.get(timeout=timeout)
                response = json.loads(res[24:])
                if response['logined']:
                    heart_data = getPacket(sequence=-1, type=Constant.TYPE_MODE)
                    b = HeartThread(socket=s, sn=sn, heart_data=heart_data)
                    sockets[sn] = s
                    queues[sn] = q
                    sns.append(sn)
                    hearThreads.append(b)
                    # print key + " logined ==SUCCESS=="
                else:
                    # print key + " logined ==FAILED=="
                    s.shutdown(2)
                    s.close()
            except Queue.Empty:
                print sn + "未响应登陆命令"
                s.shutdown(2)
                s.close()
            except Exception,e:
                print sn + "内部错误："+e.message
                s.shutdown(2)
                s.close()

        t = threading.Thread(target=a,args=(sn,res,timeout))
        ts.append(t)
        t.start()
        # if not flag:
        #      print "未搜索到此终端："+sn
    for t in ts:
        t.join()
    for i in hearThreads:
        i.start()
    self.sockets = sockets
    self.queues = queues
    self.sns = sns
    self.hearThreads = hearThreads
    print "登陆的屏体：共" + str(len(sns)) + "个",
    print sns
    nolog = list(set(searchedSn)-set(sns))
    print "未登陆成功的屏体：共"+str(len(nolog))+"个",
    print nolog
    self.assertTrue(sns,"未能登陆任何屏体")
    if len(searchedSn)==len(sns) :
        self.isLoginAll = True
    else:
        self.isLoginAll = False

def logIns(self,timeout=8):
    logins(self,timeout=timeout,tcpPort=Constant.TCP_SCREEN_SERVER_PORT)

def logInSys(self,timeout=8):
    logins(self,timeout=timeout,tcpPort=Constant.TCP_SYSSETTING_SERVER_PORT)


def logout(self):
    for i in self.hearThreads:
        i.stop()
    for i in self.sockets.values():
        i.shutdown(2)
        i.close()


        
    
    
    






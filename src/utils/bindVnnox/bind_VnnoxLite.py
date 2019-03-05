#encoding=utf-8
'''
Created on 2018年10月29日

@author: linhuajian
'''
import copy
import threading
import time

import json
import requests
from urllib3.exceptions import InsecureRequestWarning

from constant.constant import Constant
from utils.common.common import sendGetCommand, sendSetCommand, getConf, setConf
from utils.bindVnnox.delete_liteplayer import rq_Logon, unBind_vonnoxLite
from utils.vnnoxLite.vnnoxLite_interface import rq_vnnoxLiteplayer, rq_playerIdentifier, rq_PlayerProgramProgress

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

u'''获取播放器列表 '''
def get_vnnoxLiteplayer(url,username,password):
    res = rq_vnnoxLiteplayer(url,username,password)
    print res
    if "10000" in res["status"]:
        print "获取播放器列表失败"
        print res
        return False
    info = {}
    for player in res['data']['playerList']:
        if not player["isUsed"]:
            info["player"] = player
            info["token"] = res['data']['token']
            return info
    if not info:
        print "没有可用的播放器"
        return False

def get_playerIdentifier(url,token):
    info = rq_playerIdentifier(url,token)
    if 10000 in info["status"]:
        return info["data"]["identifierList"][0]
    else:
        print "获取playerIdentifier失败"
        return False




def getBindInfo(self):
    '''
    回读播放器绑定信息        
    :param1   self    必须
    :return  flag bool型   是否下发成功   
    :example flag=bind_VnnoxLite(self)
'''
    result= sendGetCommand(self,Constant.WHAT_PLAYER_BINDING,Constant.TYPE_VNNOX_BINDINFO,Constant.ACTION_GET,0,data=None,timeout=10,describe="获取绑定信息")
    return result

    
def bind_vnnoxLite(self,Server_address='',username='',password=''):
    '''
    绑定lite播放器        
    :param1   self    必须
    :param2  Server_address    vnnox认证播放器地址     
    :param3  username    vnnox认证播放器用户名
    :param3  password    vnnox认证播放器密码
    :return  flag bool型   是否下发成功   
    :example1 flag=bind_VnnoxLite(self,Server_address="cn",username="linhuajian",password="123456")
    :example2 flag=bind_VnnoxLite(self,Server_address="https://api-cn.vnnox.com",username="linhuajian",password="123456")
    :example3 flag=bind_VnnoxLite(self,Server_address="China",username="linhuajian",password="123456")               
'''
    flag = True
    result = getBindInfo(self)

    bindedSn = []
    for sn in result.keys():
        info = result[sn]
        if info in [Constant.ERROR, Constant.FAILED, Constant.NOAPPLY]:
            print sn+"获取绑定vonnox信息失败"
        elif info["isBind"]:
            bindedSn.append(sn)

    if bindedSn:
        print "解绑："+str(bindedSn)

        '''获取unbind_token'''
        vnnoxlite_url_unbind = getConf("constant", "vnnoxlite_url_unbind")
        vnnoxlite_username_unbind = getConf("constant", "vnnoxlite_username_unbind")
        vnnoxlite_password_unbind = getConf("constant", "vnnoxlite_password_unbind")
        response = rq_Logon(vnnox_url=vnnoxlite_url_unbind, username=vnnoxlite_username_unbind,
                            password=vnnoxlite_password_unbind)
        self.assertTrue(10106001 in response["status"], "获取token失败")

        # setConf("data", "token_unbind", response["data"]["token"])

        threads = []
        for sn in bindedSn:
            aliasName = json.loads(getConf("searchRes",sn))["aliasName"].encode("utf-8")
            t = threading.Thread(target=unBind_vonnoxLite,args=(self,aliasName,vnnoxlite_url_unbind,vnnoxlite_username_unbind,response["data"]["token"]))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    time.sleep(1)
    print "开始绑定"
    getBindInfo(self)
    info = get_vnnoxLiteplayer(Server_address, username, password)
    if not info:
        print "info wei kong"
        return False
    #组织data
    data = {}
    data["baseUrl"] = Server_address
    data["password"] = password
    data["username"] = username
    data1 = {}
    playerList = {}
    playerList["identifier"] =""
    playerList["isUsed"] = False
    playerList["name"] = info["player"]["name"]
    playerList["playerIdentifier"] =""
    data1["playerList"] = [playerList]
    data1["token"] = info["token"]
    data["data"] = data1
    # print data
    threads2 = []
    for sn in self.sns:
        def bindLite(self,sn,data):
            #绑定vonnoxlite
            identifier = get_playerIdentifier(Server_address, info["token"])
            if identifier:
                data = copy.deepcopy(data)
                data["data"]["playerList"][0]["identifier"] = identifier
                data["data"]["playerList"][0]["playerIdentifier"] = sn.upper()
                # print identifier+":"+sn.upper()
                flag = sendSetCommand(self, Constant.WHAT_PLAYER_BINDING, Constant.TYPE_VNNOX_BINDINFO, Constant.ACTION_SET, 0,
                               data=data, sns=[sn], timeout=8, describe="绑定lite播放器")
                # print flag
            else:
                print "未获取到identifier"
                return
        t= threading.Thread(target=bindLite,args=(self,sn,data))
        threads2.append(t)
        t.start()
    for t in threads2:
        t.join()


def assertBindInfo(self,vnnoxLite_player_url,vnnoxLite_play_user):
    '''通过终端检验'''
    flag = True
    result = getBindInfo(self)
    print result
    for sn in result.keys():
        info = result[sn]
        if info in [Constant.ERROR, Constant.FAILED, Constant.NOAPPLY]:
            print sn + "获取绑定信息失败"
            flag = False
        elif not info["isBind"]:
            print sn + "未绑定"
            flag = False
        elif info["baseUrl"] != vnnoxLite_player_url or info["username"] != vnnoxLite_play_user:
            print sn + "已绑定，但绑定信息与配置文件不符"
            flag = False

    '''在vnnox端检验'''
    flag1 = True
    res = rq_PlayerProgramProgress(url=getConf("constant","vnnoxlite_url"))
    print res
    binded_player = {}
    for i in res["data"]:
        binded_player[i["name"].encode("utf-8")] = i["id"].encode("utf-8")
    lite_player = {}
    for sn in self.sns:
        aliasName = json.loads(getConf("searchRes", sn))["aliasName"].encode("utf-8")
        if aliasName in binded_player.keys():
            lite_player[aliasName] = binded_player[aliasName]
        else:
            flag1 = False
            print aliasName + "未在vnnoxlite注册成功"

    '''将player_id写入配置文件'''
    setConf("data","lite_player",json.dumps(lite_player))

    if flag and flag1:
        print "全部绑定成功"
    self.assertTrue(flag and flag1,"未全部绑定成功")






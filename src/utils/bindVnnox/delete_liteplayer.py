#coding=utf-8
'''
Created on 2018年11月5日

@author: linhuajian
'''
import requests
import json

from urllib3.exceptions import InsecureRequestWarning

from utils.common.common import getConf, setConf
from utils.vnnoxLite.vnnoxLite_interface import rq_PlayerProgramProgress, rq_Playerdelete, rq_Logon

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# def rq_Logon(self,vnnox_url='',username='',password=''):
#     '''
#     登陆Vnnox
#     :param1   self    必须
#     :param2   username  vnnox用户名
#     :param3   password  vnnox用户密码
#     :return  flag bool型   是否登陆成功
#     :example flag=rq_Logon(self,"linhuajian","ntlhj820.")
#
# '''
#     url = vnnox_url+"/Rest/Logon"
#     data = {"username":username,"password":password}
#     response = requests.post(url=url,json=data,verify = False)
#     if str(json.loads(response.text)["status"]) == "[10106001]":
#         self.vnnox_token = json.loads(response.text)["data"]["token"]
#         return True
#     else:
#         print "登陆vonnox失败： " + url + "," + username + "," + password
#         print response.text
#         return False

def unBind_vonnoxLite(self,playerName,vnnoxlite_url_unbind,vnnoxlite_username_unbind,token):

    '''获取播放器列表'''
    data = rq_PlayerProgramProgress(url=vnnoxlite_url_unbind,token=token)
    if not (10000001 in data["status"]):
        print playerName + "获取播放器列表失败"
        return False
    data = data["data"]
    '''删除播放器'''
    flag = False
    for i in range(len(data)):
        name=data[i]["name"].encode("utf-8")
        if playerName in name:
            flag = True
            id = json.loads(data[i]["id"])
            response = rq_Playerdelete(url=vnnoxlite_url_unbind,id=id,token=token)
            status = str(response["status"])
            if status != "[10000004]":
                print name + "在" + vnnoxlite_username_unbind + "账号下，解绑失败"
                return False
            else:
                return True

    if not flag:
        print playerName+"在"+vnnoxlite_username_unbind+"下未找到与此相关的播放器"
        return False




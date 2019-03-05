#coding=utf-8

'''
Created on 2018年11月5日

'''
import requests
import json
import urllib

from urllib3.exceptions import InsecureRequestWarning

from utils.common.common import getConf
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getHearders(token):
    headers = {"token": token}
    return headers


def rq_Logon(vnnox_url="", username="", password=""):
    '''
    登陆Vnnox
    :param1   vnnox_url vnnoxLite 域名
    :param2   username  vnnoxLite 用户名
    :param3  password  vnnoxLite 用户密码
    :return  type:json response
    :example response = rq_Logon(vnnox_url="https://cn.vnnoxLite.com",username="linhuajian",password="ntlhj820.")

'''

    url = vnnox_url+"/Rest/Logon"
    data = {"username":username,"password":password}
    response = requests.post(url=url,json=data,verify = False)

    return json.loads(response.text)


def rq_PlayerProgramProgress(url=getConf("constant","vnnoxlite_url"),token=getConf("data","token")):

    '''
     获取Vnnox播放器
  :return      type:json response
  :example      response = rq_PlayerProgramProgress()
'''

    headers = getHearders(token)
    response = requests.get(url= url+ "/Rest/Lite/PlayerProgramProgress", headers=headers, verify=False)
    return json.loads(response.text)


def rq_Playerdelete(url=getConf("constant","vnnoxlite_url"),id='',token=getConf("data","token")):

    '''
    删除Vnnox播放器
 :param1   id   type:int  vnnox播放器id
 :return       type:json response
 :example       response = rq_Playerdelete(id = 13388)
'''
    headers = getHearders(token)
    response = requests.delete(url= url+ "/Rest/Lite/Player/" + str(id), headers=headers,verify=False)
    return json.loads(response.text)


def rq_program(url=getConf("constant","vnnoxlite_url"),search='',offset='',limit='',sort='',sortType='',token=getConf("data","token")):

    '''
     获取Vnnox节目列表
  :param1   search
  :param2   offset
  :param3   limit
  :param4   sort
  :param5   sortType
  :return  type:json response
  :example response = rq_program(search='',offset=1,limit=20,sort='update_time',sortType='desc')

'''

    headers = getHearders(token)
    data={"search":search,"offset":offset,"limit":limit,"sort":sort,"sortType":sortType}
    data = urllib.urlencode(data)
    print data
    response = requests.get(url= url+ "/Rest/Lite/program?"+data, headers=headers, verify=False)
    return json.loads(response.text)


def rq_generatePlan(url=getConf("constant","vnnoxlite_url"),player_id='',program_id='',token=getConf("data","token")):

    '''
    发布节目
  :param1   player_id  type:list   播放器id
  :param2   program_id type:int    节目 id
  :return  type:json response
  response = rq_generatePlan(player_id=getConf("data","id").split(','),program_id=getConf("data","program_id"))

'''

    headers = getHearders(token)
    data={"player_id": player_id,"program_id":program_id }
    print data
    response = requests.post(url=url + "/Rest/Lite/generatePlan", headers=headers,json=data, verify=False)
    return json.loads(response.text)


def rq_command(url=getConf("constant","vnnoxlite_url"),task_id='',value='',player_ids='',token=getConf("data","token")):

    '''
    播放器控制
  :param1   task_id   1:重启   2: 屏幕状态控制 正常显示    3:屏幕状态控制 黑屏  4:同步播放   8: 视频源控制 HDMI   9:视频源控制 内部   16: 音量控制  17 :亮度控制
  :param2    value        type:
  :param3    player_ids   type:str(多个用 , 分隔)   播放器id
  :return  type:json response
  :example  response = rq_command(task_id=1,player_ids=getConf("data","id"))

'''

    headers = getHearders(token)
    data={"task_id": task_id, "value": value, "player_ids": player_ids}
    print data
    response = requests.post(url=url + "/Rest/Lite/command", headers=headers,json=data, verify=False)
    return json.loads(response.text)


def rq_clearMedia(url=getConf("constant","vnnoxlite_url"),player_ids='',scope='',type='',token=getConf("data","token")):

    '''
    监控 媒体清理

  :param1  player_ids type:list  播放器id
  :param2   scope   type:int  1:不包括清理正在播放的媒体 99：清理所有媒体
  :param3   type   默认值
  :return  type:json response
  :example response = rq_clearMedia(scope=1,player_ids=getConf("data","id").split(','),type="CLEAR_MEDIA")

'''

    headers = getHearders(token)
    data = {"player_ids": player_ids, "scope": scope, "type": type}
    print data
    response = requests.post(url=url + "/Rest/Lite/clearMedia", headers=headers,json=data, verify=False)
    return json.loads(response.text)


def rq_correctTime(url=getConf("constant","vnnoxlite_url"),timezone ='', type='',nodeUrl='',player_ids='',base_player_id='',group_id=0,is_base=0,is_ntp=0,token=getConf("data","token")):

    '''
     对时
  :param1  type       type:int                 1:NTP对时 2: 射频对时  3：手动对时
  :param2  nodeUrl    type:str                 cn or '': 服务器中国  us: 服务器美国   else:  自定义服务器
  :param3  timezone   type:str                 时区
  :param4 player_ids  type:str(多个用 , 分隔） 屏体 id
  :param5 base_player_id  默认值
  :param6 group_id 默认值
  :param7 is_base  默认值
  :param8 is_ntp   默认值
  :return  type:json response
  :example  response = rq_correctTime(type=3,nodeUrl='cn',player_ids=getConf("data","id"),timezone ="Asia/Shanghai")

'''

    headers = getHearders(token)
    if nodeUrl=='us':
        nodeUrl = 'us.ntp.org.cn'
    elif nodeUrl=='cn' or nodeUrl=='':
        nodeUrl='ntp1.aliyun.com'
    else:
        nodeUrl = nodeUrl

    data = {"timezone":timezone,"player_ids":player_ids,"base_player_id":base_player_id,"type":type,"group_id":group_id,"is_base":is_base,"is_ntp":is_ntp,"nodeUrl":nodeUrl}
    print data
    response = requests.post(url=url + "/Rest/Lite/correctTime/generate", headers=headers,data=json.dumps(data), verify=False)
    return json.loads(response.text)


def rq_commandHistory(url=getConf("constant","vnnoxlite_url"),player_ids='',ttid='',synPlatform='',asyPlatform='',start_time='',end_time='',status='',offset='',limit='',sort='',sortType='',token=getConf("data","token")):

    '''
     获取日志
  :param1   player_ids  type:str(多个用 , 分隔） 屏体 id
  :param2   start_time  type:y%-m%-d H:M:S  开始时间
  :param2   end_time    type:y%-m%-d H:M:S  结束时间
  :param3   ttid         控制类型  1:重启  2:屏幕状态  3:同步播放  4:视频源  8:屏体电源  9:音量  10:亮度
  :param4   synPlatform  命令来源  1
  :param5   asyPlatform  命令来源   2 : 视频源,重启 ,屏幕状态 同步播放 4 :亮度,音量,屏体电源                       vnnox (synPlatform：1 asyPlatform：2)   其它: (synPlatform:100,100,100,2   asyPlatform:100,100,100,1)
  :param6   status       执行结果   成功:1  失败:2
  :param7   offset       默认值 0
  :param8    limit       每页条数  20
  :param9    sort        默认值  start_time
  :param10   sortType    默认值  desc
  :return  type:json response
  :example response = rq_commandHistory(player_ids=getConf("data","id"),ttid=8,synPlatform=1,asyPlatform=2,start_time='2019-01-16 00:00:00',end_time='2019-01-17 23:59:59',status='1,2',offset=0,limit=20,sort='start_time',sortType='desc')

'''

    headers = getHearders(token)

    data={"player_id":player_ids,"ttid":ttid,"filters[synPlatform]":synPlatform,"filters[asyPlatform]":asyPlatform,"filters[start_time]":start_time,"filters[end_time]":end_time,"filters[status]":status,"offset":offset,"limit":limit,"sort":sort,"sortType":sortType}
    response = requests.get(url=url + "/Rest/Lite/commandHistory", headers=headers, params=data,verify=False)
    return json.loads(response.text)

def rq_profile(url=getConf("constant","vnnoxlite_url"),token=getConf("data","token")):
    headers = getHearders(token)
    url = url+"/Rest/Lite/profile"
    response = requests.get(url=url,headers=headers)
    return json.loads(response.text)


def rq_vnnoxLiteplayer(url=getConf("constant","vnnoxlite_url"),username="",password=""):
    url = url+'/Rest/Players'
    data = {"username":username,"password":password,"playerType": 2}
    #请求vnnox获取播放器列表
    response = requests.post(url=url,json=data,verify = False)
    return json.loads(response.text)

def rq_playerIdentifier(url,token):
    header = {"token": token}
    url = url + '/Rest/playerIdentifier'
    data = {"number":1}
    # 请求vnnox获取播放器列表
    response = requests.post(url=url,headers=header, json=data, verify=False)
    return json.loads(response.text)

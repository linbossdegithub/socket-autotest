#encoding=utf-8
'''
Created on 2018年11月21日

@author: linhuajian
'''
import os
import time
from constant.constant import Constant
from utils.common.ftper import uploadFile
from utils.common.fileOperation import getFileMd5,getFileSize
from utils.common.common import sendGetCommand,sendSetCommand
def listTransfer(self,programname='local_net_planl'):
    '''.
            开始传输
    :param1   self        必须
    :param2   programname        节目名称         
    :return  flag bool型   节目是否下发成功   
    :example flag = (self,programname='local_net_planl')   '''
    
    #获取播放清单md5码
    planlistname = 'planlist.json'
    programnamedir = os.path.join(os.path.abspath("../file/media"),programname )
    mediadir =  os.path.join(programnamedir,"media")
    planlistdir = os.path.join(programnamedir,"program/"+programname)
    planlistpath = os.path.join(planlistdir,planlistname)
    listpath = os.listdir(planlistdir)
    for filename in listpath:
            if "json" not in filename:
                mediapicname = filename
    mac = '089E0129007A'
    #计算清单md5
    md5 = getFileMd5(planlistpath)
    #获取节目大小
    totalSize = getFileSize(programnamedir)
    data={"deviceIdentifier":mac,"totalSize":totalSize,"type":"DEFAULT","source":1,"local":False,"solutions":{"name": programname,"identifier":md5}}
    #print data
    result = sendGetCommand(self,Constant.WHAT_PLAYLIST,Constant.TYPE_WHAT_PLAYLIST,Constant.ACTION_START,0,data=data,timeout=4,describe="开始传输")
    #print result
    Res = {}
    uploadMediaUrl = {}
    uploadUrl = {}
    for sn in self.sns:
        if result[sn]=="FAILED" or result[sn]=="ERROR":
            Res[sn] = False
            continue
        
        #上传媒体
        uploadMediaUrl[sn] = result[sn]["uploadMediaUrl"].encode("utf-8")
        #上传清单
        uploadUrl[sn] = result[sn]["appliedInfos"]["uploadUrl"].encode("utf-8")
        
    result1 = uploadFile(self,file=mediadir,user='admin',ftpdir=uploadMediaUrl)
    result2 = uploadFile(self,file=planlistdir,user='admin',ftpdir=uploadUrl)
    print "上传媒体结果:"+str(result1)
    print "上传清单结果:"+str(result2)
    for sn in self.sns:
        if result1[sn]==False or  result2[sn] == False:
            Res[sn] = False
            continue
    #清单文件路径
    planListUrl = uploadUrl[self.sns[0]]+'/'+planlistname
    #略缩图路径
    thumbnailUrl =uploadUrl[self.sns[0]]+'/'+mediapicname
    time.sleep(3)
    flag = listTransferOver(self,identifier=md5,name=programname,planListUrl=planListUrl,thumbnailUrl=thumbnailUrl)
    for sn in Res.keys():
        if  Res[sn] ==False:
            print "节目传输错误"
            return False 
    return flag

def listTransferOver(self,identifier='',name='',planListUrl='',thumbnailUrl=''):
    '''.
            结束传输
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :param3   name               type:str     播放清单的名称
    :param4   planListUrl        type:str       planlist的路径
    :param5   thumbnailUrl    type:str       播放缩略图路径
    :return  flag bool型   是否结束传输成功   
    :example flag = Listtransfer_over(self,identifier,name,planListUrl,thumbnailUrl)
    '''
    data={"playImmediately":True,"confirmedInfos":{ "identifier":identifier,"name": name,"planListUrl":planListUrl,"thumbnailUrl":thumbnailUrl}}
    print data
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,Constant.TYPE_WHAT_PLAYLIST,Constant.ACTION_END,0,data=data,timeout=4,describe="结束传输")
    return flag

def listPlay(self,identifier=''):
    '''
            清单播放
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :return  flag bool型   是否播放成功   
    :example flag = ListPlay(self,identifier='')
    '''
    data={"identifier":identifier}
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,0x02,Constant.ACTION_START,0,data=data,timeout=4,describe="清单播放")
    return flag
def listPaused(self,identifier=''):
    '''
            清单暂停播放
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :return  flag bool型   是否暂停播放成功   
    :example flag = ListPaused(self,identifier='')
    '''
    data={"identifier":identifier}
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,0x02,Constant.ACTION_PAUSE,0,data=data,timeout=4,describe="清单暂停播放")
    return flag
def listNotify(self,identifier=''):
    '''
            清单恢复播放
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :return  flag bool型   是否恢复播放成功   
    :example flag = ListNotify(self,identifier='')
    '''
    data={"identifier":identifier}
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,0x02,Constant.ACTION_NOTIFY,0,data=data,timeout=4,describe="清单恢复播放")
    return flag
def listStop(self,identifier=''):
    '''
            清单停止播放
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :return  flag bool型   是否停止播放成功   
    :example flag = ListStop(self,identifier='')
    '''
    data={"identifier":identifier}
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,0x02,Constant.ACTION_STOP,0,data=data,timeout=4,describe="清单停止播放")
    return flag

def listCheck(self):
    '''
            清单回读
    :param1   self        必须
    :return  result     type：dict       
    :example result = ListCheck(self)
    '''
    result = sendGetCommand(self,Constant.WHAT_PLAYLIST,0x01,Constant.ACTION_GET,0,data=None,timeout=4,describe="清单播放")
    print  result
    self.identifier=[]
    self.name=[]
    self.thumbnailUrl=[]
    self.statusCode=[]
    self.source=[]
    for playlist in range(len(result["programInfos"])):
        self.identifier.append(result["programInfos"][playlist]["identifier"])
        self.name.append(result["programInfos"][playlist]["name"])
        self.thumbnailUrl.append(result["programInfos"][playlist]["thumbnailUrl"])
        self.statusCode.append(result["programInfos"][playlist]["statusCode"])
        self.source.append(result["programInfos"][playlist]["source"])
    print self.identifier
    print self.name
    print self.thumbnailUrl
    print  self.statusCode
    print self.source
    return result

def listDelete(self,identifier='' ,name=''):
    '''
            清单删除
    :param1   self        必须
    :param2   identifier          type:str      唯一标识码
    :param3        name   清单名称
    :return  flag bool型   是否停止播放成功   
    :example flag = ListDelete(self,identifier='' ,name=''):
    '''
    data={"solutions": [{"identifier":identifier,"name": name }]}
    flag = sendSetCommand(self,Constant.WHAT_PLAYLIST,0x01,Constant.ACTION_DELETE,0,data=data,timeout=4,describe="清单删除")
    return flag
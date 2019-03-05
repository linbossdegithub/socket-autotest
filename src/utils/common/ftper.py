#coding=utf8
'''
Created on 2018.12.5
@author: chenyongfa
'''
import json
from ftplib import FTP
import os

from utils.common.common import getConf


def uploadFile(self,user='',file='',ftpdir={},sns=None):
    '''
            上传文件
    :param1   self        必须
    :param2   file        要上传文件(绝对路径)
    :param4   ftpdir      T卡ftp服务器目录(绝对路径) 字典或者字符串
    :param5   user        用户名
    :return  Flag         bool 是否全部上传成功  
    :example flag=uploadFile(self,file='',sn=[],user='',ftpdir=''):
    '''
    if sns==None:
        sns = self.sns
    if user=="admin":
        portName = "ftpPort"
    elif user=="supervisor":
        portName = "syssetFtpPort"
    else:
        print "ftp用户名不存在"
    result = {}
    for sn in sns:
        if isinstance(ftpdir, dict):
            if ftpdir[sn]=="FAILED":
                result[sn] = False
                print "获取目录有失败的"
                continue
        res = json.loads(getConf("searchRes",sn))
        ip = res["addr"]
        port =  res[portName]        
        passwordkey = res["key"].encode("utf-8")
        password = sn[-8:]+'@'+passwordkey
        try:
            ftp=FTP()
            ftp.connect(ip,port)
            ftp.login(user,password)
            bufsize = 1024
            if isinstance(ftpdir, dict):
                ftppath = ftpdir[sn]
            elif isinstance(ftpdir, str):
                ftppath = ftpdir
            else:
                raise TypeError("参数fitdir类型错误")
            if os.path.isfile(file):
                filename = os.path.basename(file)
                file_handler = open(file,'rb')
                ftpabsfile = ftppath+'/'+filename
                
                ftp.storbinary('STOR %s' % ftpabsfile,file_handler,bufsize)
                file_handler.close()
                result[sn] = True
            else:
                filenames = os.listdir(file)
                for filename in filenames:
                    ftpabsfile = ftppath+'/'+filename
                    localabsfile = file+'\\'+filename
                    if not os.path.isfile(localabsfile):
                        print localabsfile
                        print "不是一个文件"
                        continue
                    file_handler = open(localabsfile, 'rb')
                    ftp.storbinary('STOR %s' % ftpabsfile, file_handler, bufsize)
                    file_handler.close()
                    result[sn] = True
        except Exception,e:
            result[sn] = False
            print sn + ":"+e.message
        finally:
            ftp.quit()

    return result


def downloadFile(self,user='',filepath='',ftpfiles={},filetype='png'):
    '''
     下载文件
    :param1   self        必须
    :param2   user        用户名
    :param3   filepath    本地存放目录
    :param4   ftpfile      需下载的文件的绝对路径
    :return  Flag  bool    
    :example flag = downloadFile(self,user='',filepath='',ftpfile='')
    '''
    if user=="admin":
        portName = "ftpPort"
    elif user=="supervisor":
        portName = "syssetFtpPort"
    else:
        print "ftp用户名不存在"
    result = {}
    for sn in self.sns:
        if ftpfiles[sn]=="FAILED":
            result[sn] = False
            continue
        try:
            res = json.loads(getConf("searchRes",sn))
            ip = res["addr"]
            port = res[portName]
            passwordkey = res["key"]
            password = str(sn)[-8:]+'@'+passwordkey
            ftp=FTP()
            ftp.connect(ip,port)
            ftp.login(user,password)
            bufsize = 1024
            filename = sn+"."+filetype
            file = os.path.join(filepath,filename)
            if os.path.exists(file):
                os.remove(file)
            ftpfile = ftpfiles[sn]
            file_handler = open(file, 'wb')
            ftp.retrbinary("RETR %s" % (ftpfile), file_handler.write,bufsize)
            file_handler.close()
            result[sn] = True
        except Exception,e:
            result[sn] = False
            print sn + ":" + e.message
        finally:
            ftp.quit()
    return result
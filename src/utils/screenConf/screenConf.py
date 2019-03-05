#encoding=utf-8
'''
Created on 2018年11月19日

@author: linhuajian
'''
from constant.constant import Constant
from utils.common.common import  sendGetCommand, sendSetCommand
def confScreen(self,portNumber=1,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=0):
    '''
            设置配屏信息
    :param1   self        必须
    :param2   portNumber  网口数量(1-2)
    :param3   width        接收卡大小宽度
    :param4   height       接收卡大小高度
    :param5   xCount       X方向上接收卡个数
    :param6   yCount       Y方向上接收卡个数
    :param7   xOffset      X轴偏移
    :param8   yOffset      Y轴偏移
    :param9   orders       连接顺序 (0-7)
    :param10  portIndex    网口序号(0-1)
    :return  flag bool型   是否下发成功   
    :example1 flag = screenConf(self,portNumber=1,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=0)
    :example2 flag = screenConf(self,portNumber=2,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=1)
                     
    '''
    data={"screenAttributes":[{"id": 0,"screenSource": 0,"xCount": xCount,"yCount": yCount,"xOffset": xOffset,"yOffset": yOffset,"portNumber": portNumber,"orders":orders,"scanInfos": [{"width":width,"height":height,"x": 0,"y": 0,"xInPort": 0,"yInPort": 0,"portIndex": portIndex,"connectIndex": 0}]}]}
    flag = sendSetCommand(self,Constant.WHAT_SCREEN_ATTRIBUTE,Constant.TYPE_SCREEN_ATTR,Constant.ACTION_SET,0,data=data,timeout=10,describe="screenConf")
    return flag

def getScreenConfinfo(self,portNumber=1,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=0):
    '''
        获取配屏信息         
    :param1   self        必须
    :param2   portNumber  网口数量(1-2)
    :param3   width        接收卡大小宽度
    :param4   height       接收卡大小高度
    :param5   xCount       X方向上接收卡个数
    :param6   yCount       Y方向上接收卡个数
    :param7   xOffset      X轴偏移
    :param8   yOffset      Y轴偏移
    :param9   orders       连接顺序 (0-7)
    :param10  portIndex    网口序号(0-1)
    :return  flag bool型   获取信息与配置信息是否一致
    :example1 flag = screenConfinfo(self,portNumber=1,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=0)
    :example2 flag = screenConfinfo(self,portNumber=2,width=64,height=32,xCount=1,yCount=1,xOffset=0,yOffset=0,orders=[1],portIndex=1)                    
'''
    RES = sendGetCommand(self,Constant.WHAT_SCREEN_ATTRIBUTE,Constant.TYPE_SCREEN_ATTR,Constant.ACTION_GET,0,data=None,timeout=5,describe="screenConfinfo")
    print RES
    flag = True
    flagdict = {}
    for sn in self.sns:
        if  RES[sn]['screenAttributes'][0]["scanInfos"][0]['height']!=height and \
            RES[sn]['screenAttributes'][0]["scanInfos"][0]['width']!=width and \
            RES[sn]['screenAttributes'][0]['yOffset']!=yOffset and \
            RES[sn]['screenAttributes'][0]['xOffset']!=xOffset and \
            RES[sn]['screenAttributes'][0]['orders']!=orders and \
            RES[sn]['screenAttributes'][0]['xCount']!=xCount and  \
            RES[sn]['screenAttributes'][0]['yCount']!=yCount :
            flag = False
            flagdict[sn] = False
        else :
            flagdict[sn] = True
    print flagdict
    return flag
    
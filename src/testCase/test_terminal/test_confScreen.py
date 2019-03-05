#encoding=utf-8
'''
Created on 2018年11月19日

@author: linhuajian
'''
import time
import unittest
from utils.login.search_login import logIns, logout
from utils.screenConf.screenConf import confScreen,getScreenConfinfo

class ConfScreen(unittest.TestCase):
    def setUp(self):
        logIns(self)
        
    def test_confScreen(self):
        portNumber=1
        width=64
        height=32
        xCount=1
        yCount=1
        xOffset=0
        yOffset=0
        orders=[1]
        portIndex=0
       
        u'''step1: 发送批量配屏命令'''
        flag = confScreen(self,portNumber=portNumber,width=width,height=height,xCount=xCount,yCount=yCount,xOffset=xOffset,yOffset=yOffset,orders=orders,portIndex=portIndex)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag, "批量配屏失败")
        
        u'''step2: 回读批量配屏结果'''
        flag = getScreenConfinfo(self,portNumber=portNumber,width=width,height=height,xCount=xCount,yCount=yCount,xOffset=xOffset,yOffset=yOffset,orders=orders,portIndex=portIndex)
        u'''check2: 回读结果是否正确 '''
        self.assertTrue(flag, "批量配屏回读失败")
        
        self.assertTrue(self.isLoginAll,"有未登陆的终端")
        time.sleep(1)

    def tearDown(self):
        logout(self)

if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(ConfScreen("test_confScreen"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
    
    
    
    
    
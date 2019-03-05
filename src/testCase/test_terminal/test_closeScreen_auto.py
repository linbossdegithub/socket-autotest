#coding=utf-8
'''
Created on 2018.10.15
@author: chenyongfa
'''
from utils.common.common import getNextTime
from utils.screenPower.getScreenPowerState import getScreenPowerState, assertPowerState
from utils.common.getPictureType import getPictureResult
import time
import unittest
from utils.screenPower.screenPower_auto import openCloseScreenAuto
from utils.login.search_login import logIns, logout
from utils.screenPower.setScreenPowerModel import setScreenPowerModel_AUTO

class CloseScreenAuto(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_autoChangeScreenState(self):
        '''step1:将开关屏模式设置为自动'''
        flag = setScreenPowerModel_AUTO(self)
        '''check1:命令是否发送成功'''
        self.assertTrue(flag,"设置开关屏模式为自动的命令未发送成功")
        '''step2:设置开关屏策略:一分钟后关屏，两分钟后开屏'''
        time1 = getNextTime(seconds=10)
        time2 = getNextTime(seconds=20)
        flag = openCloseScreenAuto(self,open=[[0,time2,True]],close=[[0,time1,True]])
        '''check2:命令是否发送成功'''
        self.assertTrue(flag, "设置开关屏策略的命令未发送成功")
        
        '''step3:13s后获取屏体状态'''
        time.sleep(13)
        res = getScreenPowerState(self)
        print res
        '''check3:查看屏体状态是否为关'''
        assertPowerState(self, res, "CLOSE")
        
        '''step4: 截图'''
        flag=getPictureResult(self)
        '''check4: 截图判断 '''
        self.assertTrue(flag == 0 or flag == 1, "截图存在开屏的状态")
        
        '''step5:20s后获取屏体状态'''
        time.sleep(13)
        res = getScreenPowerState(self)
        '''check5:查看屏体状态是否为开'''
        assertPowerState(self, res, "OPEN")
        
        '''step6: 截图'''
        flag=getPictureResult(self)
        '''check6: 截图判断 '''
        self.assertTrue(flag == 2, "截图为关屏")

        self.assertTrue(self.isLoginAll,"有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(CloseScreenAuto("test_autoChangeScreenState"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

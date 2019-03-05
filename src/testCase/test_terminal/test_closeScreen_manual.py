#coding=utf-8
'''
Created on 2018.10.15
@author: chenyongfa
'''
import time
import unittest
from utils.common.getPictureType import getPictureResult
from utils.login.search_login import logIns, logout, searchT
from utils.screenPower.getScreenPowerState import getScreenPowerState, assertPowerState
from utils.screenPower.screenPower_manual import openScreenManual, closeScreenManual
from utils.screenPower.setScreenPowerModel import setScreenPowerModel_MANUALLY

class CloseScreen(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_closeScreen(self):
        flag = getPictureResult(self)
        print flag
        u'''step1: 将开关屏设置为手动模式 '''
        flag1 = setScreenPowerModel_MANUALLY(self)

        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置手动开关屏模式 命令发送失败")
        
        u'''step2: 关屏'''
        flag2 = closeScreenManual(self)
        u'''check2: 关屏命令是否发送成功'''
        self.assertTrue(flag2, "关屏命令发送失败")
        
        u'''step3: 获取屏体的开关屏状态 '''
        res = getScreenPowerState(self)

        u'''check3: 查看屏体状态是否为  关闭 '''
        assertPowerState(self,res,"CLOSE")
        
        u'''step4: 截图'''
        flag=getPictureResult(self)
        u'''check4: 截图判断 '''
        self.assertTrue(flag == 0 or flag == 1, "截图存在开屏的状态")
        
        
        u'''step5: 开屏'''
        flag3 = openScreenManual(self)
        u'''check5: 开屏命令是否发送成功'''
        self.assertTrue(flag3, "开屏命令发送失败")

        u'''step6: 获取屏体开关屏状态'''
        res = getScreenPowerState(self)
        print res
        u'''check6: 查看屏体状态是否为开'''
        assertPowerState(self, res, "OPEN")
        time.sleep(2)
        u'''step7: 截图'''
        flag=getPictureResult(self)
        u'''check7: 截图判断 '''
        print flag
        self.assertTrue(flag==2, "截图为关屏")

        self.assertTrue(self.isLoginAll,"有未登陆的终端")
        
    def tearDown(self):
        logout(self)
        
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(CloseScreen("test_closeScreen"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

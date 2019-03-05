# coding=utf-8
'''
Created on 2018.12.13
@author: chenyongfa
'''
import time
from utils.login.search_login import logIns, logout, logInSys, searchT
from utils.update.getVersion import assertAPPVersion, assertOSVersion
from utils.update.update import updateAPP, updateOS
import unittest

class Update(unittest.TestCase):
    def setUp(self):
        # searchT()
        logInSys(self)

    def test_updateAPP(self):
        '''step1:将APP升级包放在工程的src/file/update/APP下，发送升级APP命令'''
        flag = updateAPP(self)
        '''check1:检查升级app命令是否正确'''
        self.assertTrue(flag,"APP升级命令不正确")
        '''step2:登出系统通道'''
        logout(self)
        '''step3:登陆普通通道'''
        logIns(self)
        '''check2:检查登陆终端的版本号是否正确'''
        assertAPPVersion(self)
        '''check3:检查系统通道和普通通道登陆的终端是否一致'''
        self.assertTrue(self.isLoginAll,"升级后登陆的终端与之前不一致")


    def test_updateOS(self):
        updateSns = self.sns
        '''step1:将OS升级包放在工程的src/file/update/APP下，发送升级OS命令'''
        flag = updateOS(self)
        '''check1:检查升级app命令是否正确'''
        self.assertTrue(flag, "OS升级命令不正确")
        '''step2:登出系统通道'''
        logout(self)
        '''step3:等待重启完成'''
        time.sleep(60)
        n=0
        while True:
            searchT(self)
            checkSns = self.searchRes.keys()
            if set(updateSns).issubset(set(checkSns)):
                break
            time.sleep(5)
            n+=1
            if n>30:
                break

        '''step4:登陆普通通道'''
        logIns(self)
        '''check2:检查登陆终端的版本号是否正确'''
        assertOSVersion(self)
        '''check3:检查是否全部登陆'''
        self.assertTrue(self.isLoginAll, "升级后登陆的终端与之前不一致")

    def tearDown(self):
        logout(self)

if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(Update("test_updateOS"))
    discover.addTest(Update("test_updateAPP"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
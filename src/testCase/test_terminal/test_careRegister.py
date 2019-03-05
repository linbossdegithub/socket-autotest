#coding=utf-8
'''
Created on 2018.10.15
@author: chenyongfa
'''
import time

from utils.common.common import getConf
import unittest
from utils.care.careRegister import careRegister
from utils.care.getCareInfo import getCareInfo, assertCareResult
from utils.login.search_login import logIns, logout, searchT


class CareRegister(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_careRegister(self):
        u'''step1:将T卡注册至care'''
        url = getConf("constant","care_url")
        username = getConf("constant","care_username")
        flag = careRegister(self,url,username)

        u'''check1: 是否全部注册成功'''
        self.assertTrue(flag, "未全部注册成功")
        time.sleep(3)
        u''' step2: 获取T卡care配置信息 '''
        result = getCareInfo(self)
        print result
        
        u'''check2: 查看care配置信息是否与注册信息一致 '''
        assertCareResult(self,result,url,username)

        self.assertTrue(self.isLoginAll,"有未登录的终端")
        
    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(CareRegister("test_careRegister"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
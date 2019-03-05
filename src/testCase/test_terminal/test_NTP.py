# coding=utf-8
'''
Created on 2018.11.29
@author: chenyongfa
'''
from utils.login.search_login import logIns, logout, searchT
from utils.timeSyn.getTerminalTime import getTerminalTime, assertTerminalTimeSyn
from utils.timeSyn.setManualModel import setManualModel
from utils.timeSyn.setNTPModel import setNTPModel
from utils.timeSyn.setTerminalTime import setTerminalTime
import unittest
import time


class NTPSyn(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_NTP(self):
        u'''step1: 将对时模式设置为手动'''
        flag = setManualModel(self)
        u'''check1: 命令是否发送成功'''
        self.assertTrue(flag,"设置对时模式为手动的命令未发送成功")

        u'''step2：将终端时间设置为 2018-01-01 00:00:00 '''
        flag = setTerminalTime(self)
        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag, "设置终端时间命令发送未全部成功")
        # time.sleep(2)
        u'''step3: 将对时模式设置为NTP'''
        flag = setNTPModel(self, "cn")
        u'''check3：命令是否发送成功'''
        self.assertTrue(flag, "设置终端对时模式为NTP命令发送成功")

        u'''step4:获取终端时间'''
        time.sleep(2)

        u'''check4:查看终端时间与当前时间是否一致'''
        assertTerminalTimeSyn(self)

        self.assertTrue(self.isLoginAll,"有未登陆的终端")

    def tearDown(self):
        logout(self)

if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(NTPSyn("test_NTP"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
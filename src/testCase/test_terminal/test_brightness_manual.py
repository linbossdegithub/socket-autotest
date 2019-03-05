#coding=utf-8
'''
Created on 2018.12.17
@author: gaowei
'''
import unittest
import time
from utils.login.search_login import logIns, logout, searchT
from utils.brightnessControl.setBrightnessModel import setBrightnessModel
from utils.brightnessControl.brightnessControl_Manual import setBrightness_Manual
from utils.brightnessControl.getBrightnessInfo import getBrightnessInfo, assertBrightnessInfo

class BrightnessManual(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_brightness_manual(self):

        u'''step1: 将亮度调节设置为手动模式 '''
        flag1 = setBrightnessModel(self, 'MANUALLY')
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置亮度手动模式 命令发送失败")

        u'''step2: 设置亮度值'''
        flag2 = setBrightness_Manual(self, ratio=85.0)
        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag2, "命令发送失败")

        u'''step3: 获取亮度信息 '''
        time.sleep(5)
        res = getBrightnessInfo(self)
        print res
        u'''check3: 查看亮度信息是否正确'''
        assertBrightnessInfo(self, res, ratio=85.0)

        '''check4: 是否全部登陆'''
        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)

if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(BrightnessManual("test_brightness_manual"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

# coding=utf-8
'''
Created on 2018.12.17
@author: gaowei
'''
import unittest
import time
from utils.common.common import getNextTime
from utils.login.search_login import logIns, logout, searchT
from utils.brightnessControl.setBrightnessModel import setBrightnessModel
from utils.brightnessControl.brightnessControl_Auto import setBrightnessInfo_Auto
from utils.brightnessControl.getBrightnessInfo import getBrightnessInfo, assertBrightnessInfo


class BrightnessAuto(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_brightness_auto(self):
        u'''step1: 将亮度调节设置为自动模式 '''
        flag1 = setBrightnessModel(self, 'AUTO')
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置亮度自动模式 命令发送失败")
        time.sleep(3)
        u'''step1: 设置定时亮度值：当前时间+ 10s亮度设置5%
                                  当前时间+ 25s亮度设置100%'''
        time1 = getNextTime(seconds=10)
        time2 = getNextTime(seconds=25)
        # 参数说明：重复方式，生效时间，是否生效，亮度值，有效期开始日，有效期结束日
        con_list = [['0', time1, True, '5.0', '2017-09-01 00:00:00', '4016-06-06 24:00:00'],
                    ['0', time2, True, '100.0', '2017-09-01 00:00:00', '4016-06-06 24:00:00']]

        flag2 = setBrightnessInfo_Auto(self, timing_list=con_list)
        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag2, "命令发送失败")

        u'''step3: 获取亮度信息'''
        time.sleep(15)
        res = getBrightnessInfo(self)
        print res
        u'''check3: 查看亮度信息是否正确'''
        assertBrightnessInfo(self, res, ratio=5.0)

        u'''step4: 获取亮度信息'''
        time.sleep(25)
        res = getBrightnessInfo(self)
        print res
        u'''check4: 查看亮度信息是否正确'''
        assertBrightnessInfo(self, res, ratio=100.0)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)


if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(BrightnessAuto("test_brightness_auto"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

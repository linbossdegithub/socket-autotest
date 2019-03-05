#coding=utf-8
'''
Created on 2018.12.17
@author: gaowei
'''

import unittest
import time
from utils.common.common import getNextTime
from utils.login.search_login import logIns, logout
from utils.volumeControl.volumeControl_Auto import setVolume_Auto
from utils.volumeControl.getVolumeInfo import getVolumeInfo, assertVolumeInfo


class VolumeControlAuto(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_volumecontrol_auto(self):

        u'''step1: 定时调节音量：当前时间+ 1min音量设置5%
                                当前时间+ 2min音量设置100%'''
        time1 = getNextTime(seconds=10)
        time2 = getNextTime(seconds=20)
        # 参数说明：重复方式，生效时间，是否生效，音量值，有效期开始日，有效期结束日
        con_list = [['0', time1, True, '5.0', '2017-09-01 00:00:00', '4016-06-06 24:00:00'],
                    ['0', time2, True, '100.0', '2017-09-01 00:00:00', '4016-06-06 24:00:00']]
        flag1 = setVolume_Auto(self, condition_list=con_list)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "定时调节音量 命令发送失败")

        u'''step2: 80s后获取音量配置信息 '''
        time.sleep(13)
        res = getVolumeInfo(self)
        print res

        u'''check2: 查看音量配置信息是否正确'''
        assertVolumeInfo(self, res, ratio=5.0)

        u'''step3: 100s后获取音量配置信息 '''
        time.sleep(13)
        res = getVolumeInfo(self)
        print res

        u'''check3: 查看音量配置信息是否正确'''
        assertVolumeInfo(self, res, ratio=100.0)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(VolumeControlAuto("test_volumecontrol_auto"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

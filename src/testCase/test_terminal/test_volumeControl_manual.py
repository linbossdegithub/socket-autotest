#coding=utf-8
'''
Created on 2018.12.17
@author: gaowei
'''

import unittest
from utils.login.search_login import logIns, logout
from utils.volumeControl.volumeControl_Manual import setVolume_Manual
from utils.volumeControl.getVolumeInfo import getVolumeInfo, assertVolumeInfo

class VolumeControlManual(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_volumecontrol_manual(self):

        u'''step1: 手动调节音量：音量没置22% '''
        flag1 = setVolume_Manual(self, ratio=22.0)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "手动调节音量 命令发送失败")

        u'''step2: 获取音量配置信息 '''
        res = getVolumeInfo(self)
        print res

        u'''check2: 查看音量配置信息是否正确'''
        assertVolumeInfo(self, res, ratio=22.0)

        u'''step3: 手动调节音量：音量没置77% '''
        flag2 = setVolume_Manual(self, ratio=77.0)
        u'''check3: 命令是否发送成功 '''
        self.assertTrue(flag2, "手动调节音量 命令发送失败")

        u'''step4: 获取音量配置信息 '''
        res = getVolumeInfo(self)
        print res

        u'''check4: 查看音量配置信息是否正确'''
        assertVolumeInfo(self, res, ratio=77.0)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(VolumeControlManual("test_volumecontrol_manual"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

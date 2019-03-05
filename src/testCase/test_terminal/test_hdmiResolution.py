#coding=utf-8
'''
Created on 2018.12.5
@author: gaowei
'''
import time
import unittest
from utils.login.search_login import logIns, logout
from utils.resolution.setResolution import setHDMIResolution
from utils.resolution.getResolutionInfo import getHdimResolution, assertHdmiResolutionInfo

class HdmiResolution(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_hdmiresolution(self):
        '''
           HDMI分辨率适用于T2-4G,T2,T4,T6,T8
        '''
        time.sleep(1)
        u'''step1: 设置HDMI分辨率 '''
        flag1 = setHDMIResolution(self, width=1280, height=720)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置HDMI分辨率 命令发送失败")

        u'''step2: 获取HDMI分辨率信息 '''
        res = getHdimResolution(self)
        print res
        u'''check2: 查看HDMI分辨率信息是否正确'''
        assertHdmiResolutionInfo(self, res, width=1280, height=720)

        u'''恢复默认值'''
        flag = setHDMIResolution(self, width=1920, height=1080)
        self.assertTrue(flag, "恢复HDMI默认分辨率 命令发送失败")
        res = getHdimResolution(self)
        assertHdmiResolutionInfo(self, res, width=1920, height=1080)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(HdmiResolution("test_hdmiresolution"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

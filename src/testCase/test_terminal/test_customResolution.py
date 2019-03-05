#coding=utf-8
'''
Created on 2018.12.5
@author: gaowei
'''

import unittest
from utils.login.search_login import logIns, logout, searchT
from utils.resolution.setResolution import setCustomResolution
from utils.resolution.getResolutionInfo import getCustomResolution, assertResolutionInfo


class CusResolution(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_cusresolution(self):
        '''
           内部自定义分辨率适用于T1,T2,T3,T4,T6,T8
        '''
        u'''step1: 设置内部自定义分辨率 '''
        flag1 = setCustomResolution(self, width=1344, height=500)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置内部自定义分辨率 命令发送失败")

        u'''step2: 获取内部自定义分辨率信息 '''
        res = getCustomResolution(self)
        print res
        u'''check2: 查看內部自定义分辨率信息是否正确'''
        assertResolutionInfo(self, res, width=1344, height=500)

        u'''恢复默认值'''
        flag = setCustomResolution(self, width=1920, height=1080)
        self.assertTrue(flag, "恢复自定义默认分辨率 命令发送失败")
        res = getCustomResolution(self)
        assertResolutionInfo(self, res, width=1920, height=1080)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(CusResolution("test_cusresolution"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

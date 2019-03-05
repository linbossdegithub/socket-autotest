#coding=utf-8
'''
Created on 2018.12.5
@author: gaowei
'''
import unittest
from utils.login.search_login import logIns, logout
from utils.resolution.setResolution import setCurrentResolution
from utils.resolution.getResolutionInfo import getSysResolution, assertResolutionInfo

class SysResolution(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_sysresolution(self):
        '''
           设置内部分辨率适用于T1-4G,T2-4G
           T1-4G，T2-4G不支持自定义分辨率
        '''
        u'''step1: 设置内部分辨率 '''
        flag1 = setCurrentResolution(self, resolutionValue='1920x1080p-60')
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置内部分辨率 命令发送失败")

        u'''step2: 获取內部分辨率信息 '''
        res = getSysResolution(self)
        print res

        u'''check2: 查看內部分辨率信息是否正确'''
        assertResolutionInfo(self, res, resolutionValue='1920x1080p-60')

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(SysResolution("test_sysresolution"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

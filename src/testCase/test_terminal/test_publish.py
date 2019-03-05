#encoding=utf-8
'''
Created on 2018年11月22日

@author: linhuajian
'''
import time
import unittest
from utils.login.search_login import logIns, logout,searchT
from utils.publish.publish import listTransfer
from utils.common.getPictureType import getPictureResult

class Publish(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_publish(self):
         
        u'''step1: 发送节目'''
        flag = listTransfer(self,programname='local_net_planl')
        u'''check1: 节目是否发送成功 '''
        self.assertTrue(flag, "节目发送失败")
        time.sleep(5)
        u'''step2: 截图'''
        flag=getPictureResult(self)
        u'''check2: 验证播放截图判断节目是否发送成功 '''
        self.assertTrue(flag==2, "节目播放失败")
        self.assertTrue(self.isLoginAll,"有未登陆的终端")

    def tearDown(self):
        logout(self)
        
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(Publish("test_publish"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
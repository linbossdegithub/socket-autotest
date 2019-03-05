#encoding=utf-8
'''
Created on 2018.10.29
@author: linhuajian
'''
import os
import sys
import time

from constant.constant import Constant
from utils.common.common import setConf
from utils.vnnoxLite.vnnoxLite_interface import rq_profile, rq_Logon

sys.path.append(os.path.abspath('../'))
import unittest
from utils.login.search_login import logIns, logout,searchT,getConf
from utils.bindVnnox.bind_VnnoxLite import bind_vnnoxLite, getBindInfo, assertBindInfo


class BindLite(unittest.TestCase):
    def setUp(self):
        logIns(self)
        
    def test_bindLite(self):
        u'''step1: 发送绑定lite播放器命令'''

        '''获取token，存入配置文件'''
        vnnox_url = getConf("constant", "vnnoxlite_url")
        username = getConf("constant", "vnnoxlite_username")
        password = getConf("constant", "vnnoxlite_password")

        response = rq_Logon(vnnox_url=vnnox_url,username=username,password=password)
        self.assertTrue(10106001 in response["status"],"获取token失败")
        setConf("data","token",response["data"]["token"])

        '''获取player相关信息'''
        response = rq_profile(url=vnnox_url,token=response["data"]["token"])
        print response
        vnnoxLite_play_user = response["data"]["playerAuthUsername"]
        vnnoxLite_play_password = response["data"]["playerClientSecret"]
        vnnoxLite_player_url = response["data"]["playerConnectionUrl"]

        '''绑定lite'''
        bind_vnnoxLite(self,Server_address=vnnoxLite_player_url,username=vnnoxLite_play_user,password=vnnoxLite_play_password)
        time.sleep(3)
        print "验证绑定结果，并将已绑定播放器存入配置文件"
        assertBindInfo(self,vnnoxLite_player_url,vnnoxLite_play_user)

        self.assertTrue(self.isLoginAll,"有未登陆的终端")

    def tearDown(self):
        logout(self)
        
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(BindLite("test_bindLite"))
    runner = unittest.TextTestRunner()
    runner.run(discover)
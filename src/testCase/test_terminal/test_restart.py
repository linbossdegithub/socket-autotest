#coding=utf-8
'''
Created on 2018.11.1
@author: linhuajian
'''
import os
import unittest

import time

from utils.common.common import getNextTime
from utils.common.getPictureType import assertIsPlaying
from utils.login.search_login import logIns, logout, searchT, logins
from utils.Restart.restart import restart_IMMEDIATELY,restart_CONDITIONS,assert_restartResult


class Restart(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_restart_conditions(self):
        logIns(self)
        u'''step1: 发送定时重启命令'''
        ti = getNextTime(seconds=20)
        flag=restart_CONDITIONS(self,conditions=[["1,2","15:15",False],[0,ti,True]])
        
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag, "按条件重启失败")
        print "重启命令全部发送成功"
        logout(self)
        time.sleep(20)
        u'''step2: 判断是否重启了'''
        print "判断是否重启"
        flag = assert_restartResult(self)
        
        u'''check2: 判断重启成功 '''
        self.assertTrue(flag, "重启不成功")
        print "全部重启成功"
        logins(self)
        time.sleep(3)
        u'''step3：判断截图状态'''
        print "判断截图状态"
        flag = assertIsPlaying(self)
        u'''check3: 截图判断 '''
        self.assertTrue(flag, "截图存在非播放状态")

        self.assertTrue(self.isLoginAll, "有未登陆的终端")
        
    def test_restart_immediately(self):
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        logIns(self)
        
        u'''step1: 发送立即重启命令'''
        print "发送重启命令"
        flag=restart_IMMEDIATELY(self)
        
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag, "立即重启发送失败")
        print "重启命令全部发送成功"
        logout(self)
        
        u'''step2: 判断是否重启了'''
        print "判断是否重启"
        flag = assert_restartResult(self)
        u'''check2: 判断重启成功 '''
        self.assertTrue(flag, "重启不成功")
        print "全部重启成功"
        logins(self)
        time.sleep(3)
        u'''step3：判断截图状态'''
        print "判断截图状态"
        flag = assertIsPlaying(self)
        u'''check3: 截图判断 '''
        self.assertTrue(flag, "截图存在非播放状态")
        print "截图全部为播放状态"

        self.assertTrue(self.isLoginAll,"有未登陆的终端")
        time.sleep(3)


    def tearDown(self):
        logout(self)
        print "end"
        print ""
        print ""

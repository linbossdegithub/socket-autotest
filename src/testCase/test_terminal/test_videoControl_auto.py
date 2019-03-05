#coding=utf-8
'''
Created on 2018.12.6
@author: gaowei
'''
import time
import unittest
from utils.common.common import getNextTime
from utils.login.search_login import logIns, logout
from utils.videoControl.setVideoControlModel import setVideoControl_AUTO
from utils.videoControl.videoControl_Auto import setVideoInfo_Auto
from utils.videoControl.getVideoInfo import getVideoInfo, assertVideoInfo
from utils.videoControl.videoControl_Manual import setInnerSource_Manual

class VideoControlAuto(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_videocontrol_auto(self):
        '''
           视频源切换仅适用于T2-4G, T2, T4, T6, T8
        '''

        u'''step1: 将视频源设置为定时模式 '''
        flag1 = setVideoControl_AUTO(self)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置视频源定时模式 命令发送失败")

        u'''step2: 设置视频源切换策略:一分钟后切HDMI,二分钟后切内部'''
        time_hdmi = getNextTime(seconds=10)
        time_inside = getNextTime(seconds=20)
        inside_list = [['4,5,6,7', time_inside, True]]
        hdmi_list = [['0', time_hdmi, True]]
        flag2 = setVideoInfo_Auto(self, offsetX=10, offsetY=20, isScale=True,
                                  hdmi=hdmi_list, inside=inside_list)

        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag2, "命令发送失败")

        u'''step3: 70s后获取视频源配置信息 '''
        print "等待定时任务生效"
        time.sleep(13)
        res = getVideoInfo(self)
        print res

        u'''check3: 查看视频源为HDMI，并验证其他配置信息是否正确'''
        assertVideoInfo(self, res, offsetX=10, offsetY=20, isScale=True,
                        videoMode=2, videoSource=1)

        u'''step4: 60s后获取视频源配置信息 '''
        print "等待定时任务生效"
        time.sleep(13)
        res = getVideoInfo(self)
        print res

        u'''check4: 查看视频源为内部，并验证其他配置信息是否正确'''
        assertVideoInfo(self, res, offsetX=10, offsetY=20,
                        videoMode=2, videoSource=0)

        u'''恢复默认值'''
        flag = setInnerSource_Manual(self, offsetX=0, offsetY=0)
        self.assertTrue(flag, "恢复视频源为内部 命令发送失败")
        res = getVideoInfo(self)
        print res
        assertVideoInfo(self, res, offsetX=0, offsetY=0,
                        videoMode=1, videoSource=0)

        self.assertTrue(self.isLoginAll, "有未登陆的终端")

    def tearDown(self):
        logout(self)
        
    
if __name__ == "__main__":
    discover = unittest.TestSuite()
    discover.addTest(VideoControlAuto("test_videocontrol_auto"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

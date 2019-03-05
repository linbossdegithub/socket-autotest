#coding=utf-8
'''
Created on 2018.12.6
@author: gaowei
'''

import unittest
from utils.login.search_login import logIns, logout
from utils.videoControl.setVideoControlModel import setVideoControl_HDMI_Priority
from utils.videoControl.videoControl_HdmiPriority import setvideoInfo_HDMIPriority
from utils.videoControl.getVideoInfo import getVideoInfo, assertVideoInfo
from utils.videoControl.videoControl_Manual import setInnerSource_Manual

class VideoControlHdmiPri(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_videocontrol_hdmipri(self):
        '''
           视频源切换仅适用于T2，T4，T6，T8
        '''

        u'''step1: 将视频源设置为HDMI优先模式 '''
        flag1 = setVideoControl_HDMI_Priority(self)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置视频源HDMI优先模式 命令发送失败")

        u'''step2: 设置视频源为HDMI优先并且设置相关配置项'''
        flag2 = setvideoInfo_HDMIPriority(self, offsetX=10, offsetY=20, isScale=True)

        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag2, "命令发送失败")

        u'''step3: 获取HDMI视频源配置信息 '''
        res = getVideoInfo(self)
        print res

        u'''check3: 查看视频源配置信息是否正确'''
        assertVideoInfo(self, res, videoMode=0, offsetX=10, offsetY=20, isScale=True)

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
    discover.addTest(VideoControlHdmiPri("test_videocontrol_hdmipri"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

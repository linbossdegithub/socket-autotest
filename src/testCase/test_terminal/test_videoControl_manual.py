#coding=utf-8
'''
Created on 2018.12.5
@author: gaowei
'''
import time
import unittest
from utils.login.search_login import logIns, logout
from utils.videoControl.setVideoControlModel import setVideoControl_MANUALLY
from utils.videoControl.videoControl_Manual import setInnerSource_Manual, setHDMISource_Manual
from utils.videoControl.getVideoInfo import getVideoInfo, assertVideoInfo


class VideoControlManual(unittest.TestCase):
    def setUp(self):
        logIns(self)

    def test_videocontrol_manual(self):
        '''
           视频源切换仅适用于T2，T4，T6，T8
        '''

        u'''step1: 将视频源设置为手动模式 '''
        flag1 = setVideoControl_MANUALLY(self)
        u'''check1: 命令是否发送成功 '''
        self.assertTrue(flag1, "设置视频源手动模式 命令发送失败")
        time.sleep(1)
        u'''step2: 设置视频源为HDMI并且设置相关配置项'''
        flag2 = setHDMISource_Manual(self, offsetX=30, offsetY=40, isscale=True)
        u'''check2: 命令是否发送成功'''
        self.assertTrue(flag2, "设置视频源为HDMI 命令发送失败")
        time.sleep(1)
        u'''step3: 获取HDMI视频源配置信息 '''
        res = getVideoInfo(self)
        print res
        u'''check3: 查看视频源配置信息是否正确'''
        assertVideoInfo(self, res, offsetX=30, offsetY=40, isScale=True)

        u'''step4: 设置视频源为内部并且设置相关配置项'''
        flag3 = setInnerSource_Manual(self, offsetX=10, offsetY=20)
        time.sleep(1)
        u'''check4: 命令是否发送成功'''
        self.assertTrue(flag3, "设置视频源为内部 命令发送失败")

        u'''step5: 获取內部视频源配置信息 '''
        res = getVideoInfo(self)
        print res
        u'''check5: 查看內部视频源配置信息是否正确'''
        assertVideoInfo(self, res, offsetX=10, offsetY=20,
                        videoMode=1, videoSource=0)

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
    discover.addTest(VideoControlManual("test_videocontrol_manual"))
    runner = unittest.TextTestRunner()
    runner.run(discover)

#coding=utf-8
import unittest


from testCase.test_terminal.test_NTP import NTPSyn
from testCase.test_terminal.test_bindLite import BindLite
from testCase.test_terminal.test_brightness_auto import BrightnessAuto
from testCase.test_terminal.test_brightness_manual import BrightnessManual
from testCase.test_terminal.test_careRegister import CareRegister
from testCase.test_terminal.test_closeScreen_auto import CloseScreenAuto
from testCase.test_terminal.test_closeScreen_manual import CloseScreen
from testCase.test_terminal.test_confScreen import ConfScreen
from testCase.test_terminal.test_customResolution import CusResolution
from testCase.test_terminal.test_hdmiResolution import HdmiResolution
from testCase.test_terminal.test_publish import Publish
from testCase.test_terminal.test_restart import Restart
from testCase.test_terminal.test_sysResolution import SysResolution
from testCase.test_terminal.test_videoControl_auto import VideoControlAuto
from testCase.test_terminal.test_videoControl_hdmipriority import VideoControlHdmiPri
from testCase.test_terminal.test_videoControl_manual import VideoControlManual
from testCase.test_terminal.test_volumeControl_auto import VolumeControlAuto
from testCase.test_terminal.test_volumeControl_manual import VolumeControlManual
from testCase.test_vnnoxLite.remoteControlCommand.test_brightness import Test_brightness
from testCase.test_vnnoxLite.remoteControlCommand.test_clearMedia import ClearMedia
from testCase.test_vnnoxLite.remoteControlCommand.test_generatePlan import Test_GeneratePlan
from testCase.test_vnnoxLite.remoteControlCommand.test_restart import Test_restart
from testCase.test_vnnoxLite.remoteControlCommand.test_screenStatus import Test_screenStatus
from testCase.test_vnnoxLite.remoteControlCommand.test_synchronizationTime import CorrectTime
from testCase.test_vnnoxLite.remoteControlCommand.test_synchronousPlay import Test_synchronousPlay
from testCase.test_vnnoxLite.remoteControlCommand.test_valume import Test_valume
from testCase.test_vnnoxLite.remoteControlCommand.test_videoSource import Test_videoSource


def add_sys_testCase():
    discover = unittest.TestSuite()
    # discover.addTest(Restart("test_restart_conditions"))
    # return discover
    # discover.addTest(Update("test_updateOS"))
    # discover.addTest(Update("test_updateAPP"))

    discover.addTest(ConfScreen("test_confScreen"))
    discover.addTest(Publish("test_publish"))
    discover.addTest(NTPSyn("test_NTP"))
    discover.addTest(CareRegister("test_careRegister"))
    discover.addTest(BrightnessManual("test_brightness_manual"))
    discover.addTest(BrightnessAuto("test_brightness_auto"))
    discover.addTest(CloseScreenAuto("test_autoChangeScreenState"))
    discover.addTest(CloseScreen("test_closeScreen"))
    discover.addTest(CusResolution("test_cusresolution"))
    discover.addTest(HdmiResolution("test_hdmiresolution"))
    discover.addTest(SysResolution("test_sysresolution"))
    discover.addTest(VideoControlAuto("test_videocontrol_auto"))
    discover.addTest(VideoControlHdmiPri("test_videocontrol_hdmipri"))
    discover.addTest(VideoControlManual("test_videocontrol_manual"))
    discover.addTest(VolumeControlAuto("test_volumecontrol_auto"))
    discover.addTest(VolumeControlManual("test_volumecontrol_manual"))
    discover.addTest(Restart("test_restart_conditions"))
    discover.addTest(Restart("test_restart_immediately"))
    discover.addTest(BindLite("test_bindLite"))

    '''vnnoxlite'''
    discover.addTest(CorrectTime("test_loral"))
    discover.addTest(CorrectTime("test_manual"))
    discover.addTest(CorrectTime("test_NTP_cn"))
    discover.addTest(CorrectTime("test_NTP_us"))
    discover.addTest(Test_brightness("test_brightness"))
    discover.addTest(ClearMedia("test_a"))
    discover.addTest(ClearMedia("test_b"))
    discover.addTest(Test_GeneratePlan("test_publish"))
    discover.addTest(Test_screenStatus("test_closeScreen"))
    discover.addTest(Test_screenStatus("test_openScreen"))
    discover.addTest(Test_synchronousPlay("test_synchronousPlay"))
    discover.addTest(Test_valume("test_valume"))
    discover.addTest(Test_videoSource("test_HDMI"))
    discover.addTest(Test_videoSource("test_inside"))
    discover.addTest(Test_restart("test_restart"))

    return discover

def add_press_restart():
    discover = unittest.TestSuite()
    for i in range(100):
        discover.addTest(Restart("test_restart"))
    return discover